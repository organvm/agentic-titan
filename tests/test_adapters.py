"""Tests for LLM adapters — context window config (F-23), sensitivity routing (F-24),
and Anthropic 413/529 error handling."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from adapters.base import (
    AnthropicAdapter,
    LLMConfig,
    LLMMessage,
    LLMProvider,
    LLMResponse,
    OllamaAdapter,
)
from adapters.router import (
    CLASSIFICATION_ALLOWED_PROVIDERS,
    DataClassification,
    LLMRouter,
    RoutingStrategy,
)
from agents.framework.errors import (
    LLMAdapterError,
    LLMOverloadedError,
    LLMRateLimitError,
    LLMRequestTooLargeError,
)

# ── F-23: Context window configuration ──


class TestContextWindowConfig:
    """Verify num_ctx is passed to Ollama API calls."""

    def test_default_context_window(self):
        config = LLMConfig(provider=LLMProvider.OLLAMA, model="llama3.2:3b")
        assert config.context_window == 8192

    def test_custom_context_window(self):
        config = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model="llama3.2:3b",
            context_window=32768,
        )
        assert config.context_window == 32768

    @pytest.mark.asyncio
    async def test_ollama_complete_passes_num_ctx(self):
        config = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model="llama3.2:3b",
            context_window=16384,
        )
        adapter = OllamaAdapter(config)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "message": {"content": "test response"},
            "prompt_eval_count": 10,
            "eval_count": 5,
        }

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.post = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            messages = [LLMMessage(role="user", content="Hello")]
            await adapter.complete(messages)

            # Verify num_ctx was passed in options
            call_args = mock_client.post.call_args
            request_body = call_args.kwargs.get("json") or call_args[1].get("json")
            assert request_body["options"]["num_ctx"] == 16384

    @pytest.mark.asyncio
    async def test_ollama_stream_passes_num_ctx(self):
        config = LLMConfig(
            provider=LLMProvider.OLLAMA,
            model="llama3.2:3b",
            context_window=32768,
        )
        adapter = OllamaAdapter(config)

        mock_response = AsyncMock()
        mock_response.aiter_lines = AsyncMock(return_value=AsyncMock())

        async def mock_lines():
            yield '{"message": {"content": "hi"}, "done": false}'
            yield '{"message": {"content": ""}, "done": true}'

        mock_response.aiter_lines = mock_lines

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_stream_ctx = AsyncMock()
            mock_stream_ctx.__aenter__ = AsyncMock(return_value=mock_response)
            mock_stream_ctx.__aexit__ = AsyncMock(return_value=False)
            mock_client.stream = MagicMock(return_value=mock_stream_ctx)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client_cls.return_value = mock_client

            messages = [LLMMessage(role="user", content="Hello")]
            tokens = []
            async for token in adapter.stream(messages):
                tokens.append(token)

            # Verify num_ctx was passed in options
            call_args = mock_client.stream.call_args
            request_body = call_args.kwargs.get("json") or call_args[1]["json"]
            assert request_body["options"]["num_ctx"] == 32768


# ── F-24: Sensitivity-based model routing ──


class TestDataClassification:
    """Verify data classification enum and allowed providers."""

    def test_classification_values(self):
        assert DataClassification.PUBLIC == "public"
        assert DataClassification.INTERNAL == "internal"
        assert DataClassification.CONFIDENTIAL == "confidential"
        assert DataClassification.REGULATED == "regulated"

    def test_public_allows_all_providers(self):
        allowed = CLASSIFICATION_ALLOWED_PROVIDERS[DataClassification.PUBLIC]
        assert LLMProvider.ANTHROPIC in allowed
        assert LLMProvider.OPENAI in allowed
        assert LLMProvider.OLLAMA in allowed
        assert LLMProvider.GROQ in allowed

    def test_confidential_allows_only_local(self):
        allowed = CLASSIFICATION_ALLOWED_PROVIDERS[DataClassification.CONFIDENTIAL]
        assert LLMProvider.OLLAMA in allowed
        assert LLMProvider.LOCAL in allowed
        assert LLMProvider.ANTHROPIC not in allowed
        assert LLMProvider.OPENAI not in allowed
        assert LLMProvider.GROQ not in allowed

    def test_regulated_allows_only_local(self):
        allowed = CLASSIFICATION_ALLOWED_PROVIDERS[DataClassification.REGULATED]
        assert LLMProvider.OLLAMA in allowed
        assert LLMProvider.LOCAL in allowed
        assert LLMProvider.ANTHROPIC not in allowed


class TestSensitivityRouting:
    """Verify router enforces classification constraints."""

    @pytest.mark.asyncio
    async def test_confidential_blocks_cloud_provider(self):
        router = LLMRouter(strategy=RoutingStrategy.FALLBACK)
        # Manually set up providers
        router._initialized = True
        router._providers = {
            LLMProvider.ANTHROPIC: MagicMock(available=True, supports_tools=True),
            LLMProvider.OPENAI: MagicMock(available=True, supports_tools=True),
        }
        router._fallback_chain = [LLMProvider.ANTHROPIC, LLMProvider.OPENAI]

        # Should raise because no local provider is available
        with pytest.raises(LLMAdapterError, match="No available provider"):
            router._select_provider(classification=DataClassification.CONFIDENTIAL)

    @pytest.mark.asyncio
    async def test_confidential_allows_ollama(self):
        router = LLMRouter(strategy=RoutingStrategy.FALLBACK)
        router._initialized = True
        router._providers = {
            LLMProvider.ANTHROPIC: MagicMock(
                available=True, supports_tools=True, cost_tier=3
            ),
            LLMProvider.OLLAMA: MagicMock(
                available=True, supports_tools=False, cost_tier=1
            ),
        }
        router._fallback_chain = [LLMProvider.ANTHROPIC, LLMProvider.OLLAMA]

        provider, _ = router._select_provider(
            classification=DataClassification.CONFIDENTIAL,
        )
        assert provider == LLMProvider.OLLAMA

    @pytest.mark.asyncio
    async def test_public_allows_any_provider(self):
        router = LLMRouter(strategy=RoutingStrategy.FALLBACK)
        router._initialized = True
        router._providers = {
            LLMProvider.ANTHROPIC: MagicMock(
                available=True, supports_tools=True, cost_tier=3
            ),
            LLMProvider.OLLAMA: MagicMock(
                available=True, supports_tools=False, cost_tier=1
            ),
        }
        router._fallback_chain = [LLMProvider.ANTHROPIC, LLMProvider.OLLAMA]

        provider, _ = router._select_provider(
            classification=DataClassification.PUBLIC,
        )
        # Should pick first in chain (Anthropic)
        assert provider == LLMProvider.ANTHROPIC

    @pytest.mark.asyncio
    async def test_explicit_provider_blocked_by_classification(self):
        router = LLMRouter(strategy=RoutingStrategy.FALLBACK)
        router._initialized = True
        router._providers = {
            LLMProvider.ANTHROPIC: MagicMock(available=True, supports_tools=True),
        }
        router._fallback_chain = [LLMProvider.ANTHROPIC]

        with pytest.raises(LLMAdapterError, match="not allowed"):
            await router.complete(
                [LLMMessage(role="user", content="secret data")],
                provider=LLMProvider.ANTHROPIC,
                classification=DataClassification.CONFIDENTIAL,
            )

    @pytest.mark.asyncio
    async def test_regulated_logs_audit(self, caplog):
        """Verify AUDIT log entry for regulated requests."""
        router = LLMRouter(strategy=RoutingStrategy.FALLBACK)
        router._initialized = True

        mock_adapter = AsyncMock()
        mock_adapter.complete = AsyncMock(
            return_value=LLMResponse(
                content="ok",
                model="llama3.2:3b",
                provider="ollama",
                usage={"total_tokens": 42},
            )
        )

        router._providers = {
            LLMProvider.OLLAMA: MagicMock(
                available=True, supports_tools=False, cost_tier=1
            ),
        }
        router._fallback_chain = [LLMProvider.OLLAMA]
        router._adapters = {LLMProvider.OLLAMA: mock_adapter}

        import logging

        with caplog.at_level(logging.INFO, logger="titan.adapters.router"):
            await router.complete(
                [LLMMessage(role="user", content="regulated data")],
                classification=DataClassification.REGULATED,
            )

        assert any("AUDIT" in record.message for record in caplog.records)


# ── Anthropic 413/529 error handling ──


def _make_anthropic_config() -> LLMConfig:
    """Create a minimal Anthropic adapter config for testing."""
    return LLMConfig(
        provider=LLMProvider.ANTHROPIC,
        model="claude-sonnet-4-20250514",
        api_key="test-key",  # allow-secret
    )


def _make_httpx_request() -> httpx.Request:
    """Create a dummy httpx request for exception construction."""
    return httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def _make_httpx_response(status_code: int, headers: dict | None = None) -> httpx.Response:
    """Create a minimal httpx response for exception construction."""
    resp = httpx.Response(
        status_code=status_code,
        request=_make_httpx_request(),
        headers=headers or {},
    )
    return resp


class TestAnthropicErrorTranslation:
    """Verify _translate_api_error maps Anthropic SDK errors to Titan hierarchy."""

    def test_413_request_too_large_via_typed_exception(self):
        from anthropic._exceptions import RequestTooLargeError

        response = _make_httpx_response(413)
        sdk_err = RequestTooLargeError(
            message="Request too large",
            response=response,
            body={"error": {"type": "request_too_large", "message": "Request too large"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMRequestTooLargeError)
        assert result.code == "LLM_REQUEST_TOO_LARGE"
        assert result.recoverable is False
        assert result.provider == "anthropic"

    def test_529_overloaded_via_typed_exception(self):
        from anthropic._exceptions import OverloadedError

        response = _make_httpx_response(529, headers={"retry-after": "30"})
        sdk_err = OverloadedError(
            message="Overloaded",
            response=response,
            body={"error": {"type": "overloaded_error", "message": "Overloaded"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMOverloadedError)
        assert result.code == "LLM_OVERLOADED"
        assert result.retry_after == 30
        assert result.provider == "anthropic"

    def test_529_overloaded_without_retry_after(self):
        from anthropic._exceptions import OverloadedError

        response = _make_httpx_response(529)
        sdk_err = OverloadedError(
            message="Overloaded",
            response=response,
            body={"error": {"type": "overloaded_error", "message": "Overloaded"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMOverloadedError)
        assert result.retry_after is None

    def test_429_rate_limit(self):
        from anthropic import RateLimitError

        response = _make_httpx_response(429, headers={"retry-after": "5"})
        sdk_err = RateLimitError(
            message="Rate limited",
            response=response,
            body={"error": {"type": "rate_limit_error", "message": "Rate limited"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMRateLimitError)
        assert result.retry_after == 5

    def test_413_via_status_code_fallback(self):
        """If the SDK sends a generic APIStatusError with status 413, we still catch it."""
        from anthropic import APIStatusError

        response = _make_httpx_response(413)
        sdk_err = APIStatusError(
            message="Request too large",
            response=response,
            body={"error": {"type": "request_too_large", "message": "Request too large"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMRequestTooLargeError)

    def test_529_via_status_code_fallback(self):
        """If the SDK sends a generic APIStatusError with status 529, we still catch it."""
        from anthropic import APIStatusError

        response = _make_httpx_response(529)
        sdk_err = APIStatusError(
            message="Overloaded",
            response=response,
            body={"error": {"type": "overloaded_error", "message": "Overloaded"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMOverloadedError)

    def test_other_api_status_error_becomes_generic(self):
        from anthropic import APIStatusError

        response = _make_httpx_response(500)
        sdk_err = APIStatusError(
            message="Internal server error",
            response=response,
            body={"error": {"type": "api_error", "message": "Internal server error"}},
        )

        result = AnthropicAdapter._translate_api_error(sdk_err)
        assert isinstance(result, LLMAdapterError)
        assert "HTTP 500" in str(result)

    def test_non_anthropic_error_passes_through(self):
        """Non-SDK exceptions are returned as-is (not wrapped)."""
        original = ValueError("something unrelated")
        result = AnthropicAdapter._translate_api_error(original)
        assert result is original


class TestAnthropicAdapterErrorHandling:
    """Verify AnthropicAdapter.complete() and stream() translate errors."""

    @pytest.mark.asyncio
    async def test_complete_raises_request_too_large(self):
        from anthropic._exceptions import RequestTooLargeError

        adapter = AnthropicAdapter(_make_anthropic_config())
        response = _make_httpx_response(413)
        sdk_err = RequestTooLargeError(
            message="Request too large",
            response=response,
            body={"error": {"type": "request_too_large", "message": "Request too large"}},
        )

        with patch("anthropic.AsyncAnthropic") as mock_cls:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(side_effect=sdk_err)
            mock_cls.return_value = mock_client

            with pytest.raises(LLMRequestTooLargeError):
                await adapter.complete(
                    [LLMMessage(role="user", content="x" * 1_000_000)],
                )

    @pytest.mark.asyncio
    async def test_complete_raises_overloaded(self):
        from anthropic._exceptions import OverloadedError

        adapter = AnthropicAdapter(_make_anthropic_config())
        response = _make_httpx_response(529, headers={"retry-after": "10"})
        sdk_err = OverloadedError(
            message="Overloaded",
            response=response,
            body={"error": {"type": "overloaded_error", "message": "Overloaded"}},
        )

        with patch("anthropic.AsyncAnthropic") as mock_cls:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(side_effect=sdk_err)
            mock_cls.return_value = mock_client

            with pytest.raises(LLMOverloadedError) as exc_info:
                await adapter.complete(
                    [LLMMessage(role="user", content="hello")],
                )
            assert exc_info.value.retry_after == 10

    @pytest.mark.asyncio
    async def test_stream_raises_overloaded(self):
        from anthropic._exceptions import OverloadedError

        adapter = AnthropicAdapter(_make_anthropic_config())
        response = _make_httpx_response(529)
        sdk_err = OverloadedError(
            message="Overloaded",
            response=response,
            body={"error": {"type": "overloaded_error", "message": "Overloaded"}},
        )

        with patch("anthropic.AsyncAnthropic") as mock_cls:
            mock_client = AsyncMock()
            # The stream context manager itself raises the error
            mock_stream_ctx = AsyncMock()
            mock_stream_ctx.__aenter__ = AsyncMock(side_effect=sdk_err)
            mock_client.messages.stream = MagicMock(return_value=mock_stream_ctx)
            mock_cls.return_value = mock_client

            with pytest.raises(LLMOverloadedError):
                async for _token in adapter.stream(
                    [LLMMessage(role="user", content="hello")],
                ):
                    pass  # pragma: no cover


class TestErrorHierarchyProperties:
    """Verify the new error types have correct recovery and severity metadata."""

    def test_request_too_large_is_non_retryable(self):
        err = LLMRequestTooLargeError(provider="anthropic", detail="too big")
        assert err.recoverable is False
        assert err.recovery.value == "abort"
        assert err.severity.value == "high"
        assert "too big" in str(err)

    def test_overloaded_is_retryable(self):
        err = LLMOverloadedError(provider="anthropic", retry_after=15)
        assert err.recovery.value == "retry_with_backoff"
        assert err.retry_after == 15
        assert err.severity.value == "high"

    def test_overloaded_without_retry_after(self):
        err = LLMOverloadedError(provider="anthropic")
        assert err.retry_after is None
        assert "overloaded" in str(err).lower()

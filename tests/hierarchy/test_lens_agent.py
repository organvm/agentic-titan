"""Tests for the lens agent system — hierarchy lens integration."""

import pytest

from titan.hierarchy.lens_agent import (
    LensAgent,
    LensAgentConfig,
    LensInsightTrace,
    LensLifecycle,
    LensSwarmManager,
)


@pytest.fixture
def config():
    """Create a test lens agent config."""
    return LensAgentConfig(
        lens_id="test_lens",
        name="Test Lens",
        stratum="/sys/",
        category="tooling",
        summon_when="Testing",
        system_prompt="You are a test lens.",
        capabilities=["testing"],
    )


@pytest.fixture
def agent(config):
    """Create a test lens agent."""
    return LensAgent(config)


@pytest.fixture
def manager():
    """Create a LensSwarmManager with 3 registered lenses."""
    mgr = LensSwarmManager()
    for name in ["alpha", "beta", "gamma"]:
        mgr.register_lens(LensAgentConfig(
            lens_id=name,
            name=name.title(),
            stratum="/sys/",
            category="tooling",
            summon_when="Testing",
            system_prompt=f"You are the {name} lens.",
        ))
    return mgr


class TestLensAgent:
    def test_starts_dormant(self, agent):
        assert agent.lifecycle == LensLifecycle.DORMANT

    def test_summon_transitions(self, agent):
        agent.summon("test task")
        assert agent.lifecycle == LensLifecycle.SUMMONED

    def test_summon_rejects_non_dormant(self, agent):
        agent.summon("test task")
        with pytest.raises(RuntimeError):
            agent.summon("another task")

    def test_fuse_transitions(self, agent):
        agent.summon("test task")
        agent.fuse()
        assert agent.lifecycle == LensLifecycle.FUSED

    def test_fuse_rejects_non_summoned(self, agent):
        with pytest.raises(RuntimeError):
            agent.fuse()

    def test_release_from_summoned(self, agent):
        agent.summon("test task")
        trace = agent.release(insight="key insight", critique="key critique")
        assert agent.lifecycle == LensLifecycle.RELEASED
        assert trace is not None
        assert trace.insight == "key insight"
        assert trace.critique == "key critique"

    def test_release_from_fused(self, agent):
        agent.summon("test task")
        agent.fuse()
        trace = agent.release(insight="fused insight")
        assert agent.lifecycle == LensLifecycle.RELEASED
        assert trace is not None

    def test_release_no_insight(self, agent):
        agent.summon("test task")
        trace = agent.release()
        assert trace is None

    def test_release_rejects_dormant(self, agent):
        with pytest.raises(RuntimeError):
            agent.release()

    def test_reset_to_dormant(self, agent):
        agent.summon("test")
        agent.release()
        agent.reset()
        assert agent.lifecycle == LensLifecycle.DORMANT

    def test_get_traces(self, agent):
        agent.summon("task")
        agent.release(insight="trace1")
        agent.reset()
        agent.summon("task2")
        agent.release(insight="trace2")
        traces = agent.get_traces()
        assert len(traces) == 2

    def test_agent_id_unique(self, config):
        a1 = LensAgent(config)
        a2 = LensAgent(config)
        assert a1.agent_id != a2.agent_id

    def test_to_dict(self, agent):
        d = agent.to_dict()
        assert d["lens_id"] == "test_lens"
        assert d["lifecycle"] == "dormant"
        assert "config" in d

    def test_lens_id_property(self, agent):
        assert agent.lens_id == "test_lens"

    def test_config_property(self, agent, config):
        assert agent.config is config


class TestLensInsightTrace:
    def test_to_dict(self):
        trace = LensInsightTrace(
            trace_id="t1",
            lens_id="test",
            task_context="ctx",
            insight="insight",
            critique="critique",
            confidence=0.9,
        )
        d = trace.to_dict()
        assert d["trace_id"] == "t1"
        assert d["confidence"] == 0.9
        assert "deposited_at" in d


class TestLensSwarmManager:
    def test_register_lens(self, manager):
        assert len(manager.registered_lens_ids) == 3

    def test_register_duplicate_raises(self, manager):
        with pytest.raises(ValueError):
            manager.register_lens(LensAgentConfig(
                lens_id="alpha",
                name="Dup",
                stratum="/sys/",
                category="tooling",
                summon_when="Test",
                system_prompt="dup",
            ))

    def test_summon_assembly(self, manager):
        agents = manager.summon_assembly(["alpha", "beta"], "test task")
        assert len(agents) == 2
        assert all(a.lifecycle == LensLifecycle.SUMMONED for a in agents)

    def test_summon_exceeds_cap(self, manager):
        # Register a 4th lens
        manager.register_lens(LensAgentConfig(
            lens_id="delta",
            name="Delta",
            stratum="/sys/",
            category="tooling",
            summon_when="Test",
            system_prompt="delta",
        ))
        with pytest.raises(ValueError, match="max is 3"):
            manager.summon_assembly(["alpha", "beta", "gamma", "delta"], "task")

    def test_summon_unknown_lens(self, manager):
        with pytest.raises(ValueError, match="not registered"):
            manager.summon_assembly(["nonexistent"], "task")

    def test_fuse_all(self, manager):
        agents = manager.summon_assembly(["alpha", "beta"], "task")
        manager.fuse_all(agents)
        assert all(a.lifecycle == LensLifecycle.FUSED for a in agents)

    def test_release_all_with_insights(self, manager):
        agents = manager.summon_assembly(["alpha", "beta"], "task")
        traces = manager.release_all(
            agents,
            insights={"alpha": "alpha insight", "beta": "beta insight"},
            critiques={"alpha": "alpha critique"},
        )
        assert len(traces) == 2
        assert all(a.lifecycle == LensLifecycle.RELEASED for a in agents)

    def test_release_all_without_insights(self, manager):
        agents = manager.summon_assembly(["alpha"], "task")
        traces = manager.release_all(agents)
        assert len(traces) == 0

    def test_get_active_agents(self, manager):
        manager.summon_assembly(["alpha"], "task")
        active = manager.get_active_agents()
        assert len(active) == 1
        assert active[0].lens_id == "alpha"

    def test_get_agent(self, manager):
        agent = manager.get_agent("alpha")
        assert agent is not None
        assert agent.lens_id == "alpha"

    def test_get_agent_none(self, manager):
        assert manager.get_agent("nonexistent") is None

    def test_assembly_count(self, manager):
        assert manager.assembly_count == 0
        agents = manager.summon_assembly(["alpha"], "task")
        manager.release_all(agents)
        assert manager.assembly_count == 1

    def test_resummon_after_release(self, manager):
        """Agents should auto-reset if re-summoned."""
        agents = manager.summon_assembly(["alpha"], "task1")
        manager.release_all(agents)
        agents2 = manager.summon_assembly(["alpha"], "task2")
        assert len(agents2) == 1
        assert agents2[0].lifecycle == LensLifecycle.SUMMONED

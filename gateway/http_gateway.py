"""
Thin HTTP gateway wrapping Titan MCP tools for external consumption.

Usage:
    uvicorn gateway.http_gateway:app --port 8100

Endpoints:
    POST /api/titan/route-task  → route_cognitive_task
    POST /api/titan/inquiry     → start_inquiry
    GET  /api/titan/topology    → topology/current resource
    GET  /health                → health check
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logger = logging.getLogger("titan.gateway")

app = FastAPI(
    title="Agentic Titan HTTP Gateway",
    version="0.1.0",
    description="HTTP bridge to Titan MCP tools for external systems",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stakeholder-portal-ten.vercel.app",
        "http://localhost:3000",
        "http://localhost:4321",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class RouteTaskRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=4000)
    context: str | None = None


class InquiryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=4000)
    scope: str | None = None


class TaskResult(BaseModel):
    taskId: str
    status: str  # "completed" | "failed" | "timeout"
    result: str | None = None
    model: str | None = None
    agentType: str | None = None


# ---------------------------------------------------------------------------
# Lazy MCP tool imports — avoids startup failure if titan_mcp deps missing
# ---------------------------------------------------------------------------

_mcp_server = None


def _get_server():
    global _mcp_server
    if _mcp_server is None:
        try:
            from titan_mcp.server import MCPServer

            _mcp_server = MCPServer()
        except ImportError as e:
            logger.error(f"Cannot import titan_mcp: {e}")
            raise HTTPException(
                status_code=503,
                detail="Titan MCP server module not available",
            )
    return _mcp_server


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"ok": True, "service": "titan-gateway"}


@app.post("/api/titan/route-task", response_model=TaskResult)
async def route_task(req: RouteTaskRequest):
    server = _get_server()
    task_id = str(uuid.uuid4())

    try:
        result = await server.handle_tool_call(
            "route_cognitive_task",
            {"task_description": req.query, "context": req.context or ""},
        )
        return TaskResult(
            taskId=task_id,
            status="completed",
            result=_extract_text(result),
            model=_extract_field(result, "model"),
            agentType=_extract_field(result, "agent_type"),
        )
    except Exception as e:
        logger.exception("route_cognitive_task failed")
        return TaskResult(taskId=task_id, status="failed", result=str(e))


@app.post("/api/titan/inquiry", response_model=TaskResult)
async def inquiry(req: InquiryRequest):
    server = _get_server()
    task_id = str(uuid.uuid4())

    try:
        result = await server.handle_tool_call(
            "start_inquiry",
            {"topic": req.question, "scope": req.scope or "general"},
        )
        return TaskResult(
            taskId=task_id,
            status="completed",
            result=_extract_text(result),
        )
    except Exception as e:
        logger.exception("start_inquiry failed")
        return TaskResult(taskId=task_id, status="failed", result=str(e))


@app.get("/api/titan/topology")
async def topology():
    server = _get_server()
    try:
        result = await server.handle_resource_read("topology://current")
        return {"ok": True, "topology": result}
    except Exception as e:
        logger.exception("topology read failed")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_text(result: Any) -> str | None:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        for key in ("text", "result", "content", "response"):
            if key in result and isinstance(result[key], str):
                return result[key]
        # MCP tool results have content array
        contents = result.get("content", [])
        if isinstance(contents, list):
            texts = [c.get("text", "") for c in contents if isinstance(c, dict)]
            joined = "\n".join(texts).strip()
            if joined:
                return joined
    if isinstance(result, list):
        texts = [c.get("text", "") for c in result if isinstance(c, dict)]
        return "\n".join(texts).strip() or None
    return str(result) if result else None


def _extract_field(result: Any, field: str) -> str | None:
    if isinstance(result, dict):
        val = result.get(field)
        return str(val) if val else None
    return None

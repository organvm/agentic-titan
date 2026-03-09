"""Lens Agent — base class for hierarchy lens agents in the swarm.

Each lens agent encodes the logic of one organizational lens from the
universal hierarchy. Lens agents have lifecycle hooks for assembly/release,
deposit stigmergic traces (insights that persist after the lens is released),
and participate in fission-fusion dynamics.

Integration points:
- hive/fission_fusion.py: FissionFusionState for dense/sparse transitions
- hive/stigmergy.py: PheromoneTrace for depositing persistent insights
- hive/criticality.py: PhaseTransition for stratum-shift detection
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

logger = logging.getLogger("titan.hierarchy.lens_agent")


class LensLifecycle(StrEnum):
    """Lifecycle states for a lens agent."""

    DORMANT = "dormant"        # Available but not summoned
    SUMMONED = "summoned"      # Active, interrogating
    FUSED = "fused"            # In multi-lens synthesis
    RELEASING = "releasing"    # Depositing traces before release
    RELEASED = "released"      # Insight absorbed, lens dismissed


@dataclass
class LensAgentConfig:
    """Configuration for a lens agent, loaded from titan.yaml specs."""

    lens_id: str
    name: str
    stratum: str
    category: str
    summon_when: str
    system_prompt: str
    capabilities: list[str] = field(default_factory=list)
    max_turns: int = 30
    release_when: str = "Insight absorbed into task output"


@dataclass
class LensInsightTrace:
    """An insight trace deposited by a lens agent into the stigmergy layer.

    These persist after the lens is released, informing future assemblies
    about what this lens discovered in previous invocations.
    """

    trace_id: str
    lens_id: str
    task_context: str
    insight: str
    critique: str
    confidence: float         # 0.0 to 1.0
    deposited_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Export as dictionary for stigmergy deposit."""
        return {
            "trace_id": self.trace_id,
            "lens_id": self.lens_id,
            "task_context": self.task_context,
            "insight": self.insight,
            "critique": self.critique,
            "confidence": self.confidence,
            "deposited_at": self.deposited_at.isoformat(),
        }


class LensAgent:
    """Base class for hierarchy lens agents.

    Each lens agent has:
    - A system prompt encoding the lens's logic (from research documents)
    - A critique function
    - Assembly/release lifecycle hooks
    - Connection to the stigmergy layer for depositing traces
    """

    def __init__(self, config: LensAgentConfig) -> None:
        self._config = config
        self._lifecycle = LensLifecycle.DORMANT
        self._traces: list[LensInsightTrace] = []
        self._current_task: str | None = None
        self._agent_id = f"lens_{config.lens_id}_{uuid.uuid4().hex[:8]}"

    @property
    def agent_id(self) -> str:
        """Unique agent ID for this lens instance."""
        return self._agent_id

    @property
    def lens_id(self) -> str:
        """The hierarchy lens ID."""
        return self._config.lens_id

    @property
    def lifecycle(self) -> LensLifecycle:
        """Current lifecycle state."""
        return self._lifecycle

    @property
    def config(self) -> LensAgentConfig:
        """Agent configuration."""
        return self._config

    def summon(self, task_description: str) -> None:
        """Summon this lens for a task.

        Transitions from DORMANT to SUMMONED.

        Args:
            task_description: The task to interrogate through this lens.

        Raises:
            RuntimeError: If the lens is not in DORMANT state.
        """
        if self._lifecycle != LensLifecycle.DORMANT:
            raise RuntimeError(
                f"Cannot summon lens '{self.lens_id}' — "
                f"current state is {self._lifecycle.value}"
            )
        self._lifecycle = LensLifecycle.SUMMONED
        self._current_task = task_description
        logger.info(f"Summoned lens: {self.lens_id} for task: {task_description[:50]}")

    def fuse(self) -> None:
        """Enter fused state for multi-lens synthesis.

        Transitions from SUMMONED to FUSED.

        Raises:
            RuntimeError: If not in SUMMONED state.
        """
        if self._lifecycle != LensLifecycle.SUMMONED:
            raise RuntimeError(
                f"Cannot fuse lens '{self.lens_id}' — "
                f"current state is {self._lifecycle.value}"
            )
        self._lifecycle = LensLifecycle.FUSED
        logger.info(f"Fused lens: {self.lens_id}")

    def release(self, insight: str = "", critique: str = "") -> LensInsightTrace | None:
        """Release the lens, depositing a stigmergic trace.

        Transitions to RELEASING then RELEASED.

        Args:
            insight: The insight to deposit as a trace.
            critique: The critique to deposit.

        Returns:
            The deposited trace, or None if no insight provided.
        """
        if self._lifecycle not in (LensLifecycle.SUMMONED, LensLifecycle.FUSED):
            raise RuntimeError(
                f"Cannot release lens '{self.lens_id}' — "
                f"current state is {self._lifecycle.value}"
            )

        self._lifecycle = LensLifecycle.RELEASING

        trace = None
        if insight:
            trace = LensInsightTrace(
                trace_id=f"insight_{self.lens_id}_{uuid.uuid4().hex[:8]}",
                lens_id=self.lens_id,
                task_context=self._current_task or "",
                insight=insight,
                critique=critique,
                confidence=0.8,
            )
            self._traces.append(trace)
            logger.info(f"Deposited insight trace from lens: {self.lens_id}")

        self._lifecycle = LensLifecycle.RELEASED
        self._current_task = None
        logger.info(f"Released lens: {self.lens_id}")
        return trace

    def reset(self) -> None:
        """Reset the lens back to DORMANT for reuse."""
        self._lifecycle = LensLifecycle.DORMANT
        self._current_task = None

    def get_traces(self) -> list[LensInsightTrace]:
        """Get all insight traces deposited by this lens."""
        return list(self._traces)

    def to_dict(self) -> dict[str, Any]:
        """Export agent state as dictionary."""
        return {
            "agent_id": self._agent_id,
            "lens_id": self.lens_id,
            "lifecycle": self._lifecycle.value,
            "current_task": self._current_task,
            "traces_count": len(self._traces),
            "config": {
                "name": self._config.name,
                "stratum": self._config.stratum,
                "category": self._config.category,
            },
        }


class LensSwarmManager:
    """Manages a swarm of lens agents for dynamic assembly.

    Coordinates the summoning, fusing, and releasing of lens agents
    within the fission-fusion topology. The manager enforces the
    cognitive load limit (max 3 simultaneous lenses).
    """

    MAX_SIMULTANEOUS = 3  # Hard cognitive load cap

    def __init__(self) -> None:
        self._agents: dict[str, LensAgent] = {}
        self._assembly_history: list[dict[str, Any]] = []

    def register_lens(self, config: LensAgentConfig) -> LensAgent:
        """Register a new lens agent.

        Args:
            config: Configuration for the lens agent.

        Returns:
            The created LensAgent.

        Raises:
            ValueError: If a lens with this ID is already registered.
        """
        if config.lens_id in self._agents:
            raise ValueError(f"Lens '{config.lens_id}' already registered")
        agent = LensAgent(config)
        self._agents[config.lens_id] = agent
        return agent

    def summon_assembly(
        self,
        lens_ids: list[str],
        task_description: str,
    ) -> list[LensAgent]:
        """Summon multiple lenses for a task assembly.

        Enforces the cognitive load cap (max 3).

        Args:
            lens_ids: IDs of lenses to summon.
            task_description: The task to interrogate.

        Returns:
            List of summoned LensAgent instances.

        Raises:
            ValueError: If too many lenses requested or lens not found.
        """
        if len(lens_ids) > self.MAX_SIMULTANEOUS:
            raise ValueError(
                f"Cannot summon {len(lens_ids)} lenses — "
                f"max is {self.MAX_SIMULTANEOUS}"
            )

        summoned: list[LensAgent] = []
        for lid in lens_ids:
            if lid not in self._agents:
                raise ValueError(f"Lens '{lid}' not registered")
            agent = self._agents[lid]
            if agent.lifecycle != LensLifecycle.DORMANT:
                agent.reset()
            agent.summon(task_description)
            summoned.append(agent)

        return summoned

    def fuse_all(self, agents: list[LensAgent]) -> None:
        """Fuse all summoned agents into synthesis mode.

        Args:
            agents: List of summoned agents to fuse.
        """
        for agent in agents:
            if agent.lifecycle == LensLifecycle.SUMMONED:
                agent.fuse()

    def release_all(
        self,
        agents: list[LensAgent],
        insights: dict[str, str] | None = None,
        critiques: dict[str, str] | None = None,
    ) -> list[LensInsightTrace]:
        """Release all agents in an assembly, collecting traces.

        Args:
            agents: Agents to release.
            insights: Dict mapping lens_id to insight string.
            critiques: Dict mapping lens_id to critique string.

        Returns:
            List of deposited insight traces.
        """
        insights = insights or {}
        critiques = critiques or {}
        traces: list[LensInsightTrace] = []

        for agent in agents:
            if agent.lifecycle in (LensLifecycle.SUMMONED, LensLifecycle.FUSED):
                trace = agent.release(
                    insight=insights.get(agent.lens_id, ""),
                    critique=critiques.get(agent.lens_id, ""),
                )
                if trace:
                    traces.append(trace)

        # Record in history
        self._assembly_history.append({
            "timestamp": datetime.now(UTC).isoformat(),
            "lenses": [a.lens_id for a in agents],
            "traces_deposited": len(traces),
        })

        return traces

    def get_active_agents(self) -> list[LensAgent]:
        """Get all agents not in DORMANT or RELEASED state."""
        return [
            a for a in self._agents.values()
            if a.lifecycle not in (LensLifecycle.DORMANT, LensLifecycle.RELEASED)
        ]

    def get_agent(self, lens_id: str) -> LensAgent | None:
        """Get a specific lens agent by ID."""
        return self._agents.get(lens_id)

    @property
    def registered_lens_ids(self) -> list[str]:
        """List all registered lens IDs."""
        return list(self._agents.keys())

    @property
    def assembly_count(self) -> int:
        """Number of assemblies performed."""
        return len(self._assembly_history)

"""Hierarchy lens integration for the agent swarm.

Bridges universal-node-network hierarchy lenses into the agentic-titan
fission-fusion topology, enabling lenses to be summoned as agents that
fuse for multi-perspective analysis and fission back when complete.
"""

from .lens_agent import LensAgent, LensAgentConfig, LensSwarmManager

__all__ = ["LensAgent", "LensAgentConfig", "LensSwarmManager"]

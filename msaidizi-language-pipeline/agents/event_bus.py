"""
Agent Event Bus — Singleton pub/sub for agent runtime events.

This module provides the central event bus that connects the three-tier
memory system to the agent runtime. All agent lifecycle events flow
through this bus.

Architecture:
  Agent → AgentEventBus → [WorkingMemory, EpisodicMemory, LongTermMemory]
  Agent → AgentEventBus → [Observability, Feedback, Reflexion]

The bus is a singleton — all agents and memory tiers share the same instance.
This ensures memory consolidation, decay, and retrieval work across the
entire agent runtime.

Event types:
  - INTERACTION_START/END: User conversation lifecycle
  - OBSERVATION: New sensory input
  - DECISION: Agent chose an action
  - RESULT: Action completed (success/failure)
  - REFLECTION: Agent reflecting on outcomes
  - MEMORY_CONSOLIDATION: Periodic memory maintenance
  - ERROR: Something went wrong

@author Angavu Intelligence — Fix Swarm 3 (Memory System Wiring)
"""

from __future__ import annotations

import logging
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Types of events on the agent event bus."""

    # User interaction lifecycle
    INTERACTION_START = "interaction_start"
    INTERACTION_END = "interaction_end"

    # Agent processing events
    OBSERVATION = "observation"        # New input observed
    ORIENTATION = "orientation"        # Agent updated its mental model
    DECISION = "decision"              # Agent chose an action
    ACTION_START = "action_start"      # Action execution began
    ACTION_RESULT = "action_result"    # Action completed with result
    REFLECTION = "reflection"          # Agent reflecting on outcome

    # Memory events
    MEMORY_STORE = "memory_store"      # Something stored in memory
    MEMORY_RECALL = "memory_recall"    # Something recalled from memory
    MEMORY_CONSOLIDATION = "memory_consolidation"  # Periodic maintenance

    # System events
    DIALECT_DETECTED = "dialect_detected"
    CODE_SWITCH_DETECTED = "code_switch_detected"
    TRUST_UPDATE = "trust_update"
    AUTONOMY_CHANGE = "autonomy_change"
    ERROR = "error"


@dataclass
class AgentEvent:
    """An event on the agent event bus."""

    event_type: EventType
    timestamp: float = field(default_factory=time.time)
    agent_id: Optional[str] = None
    user_id_hash: Optional[str] = None
    dialect: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def age_seconds(self) -> float:
        """How old this event is in seconds."""
        return time.time() - self.timestamp


# Type alias for event handlers
EventHandler = Callable[[AgentEvent], None]


class AgentEventBus:
    """
    Singleton event bus for the Msaidizi agent runtime.

    All memory tiers, observability systems, and feedback loops
    subscribe to this bus to receive agent events.

    Thread-safe: uses a lock for concurrent access from multiple
    agent coroutines.

    Usage:
        bus = AgentEventBus.get_instance()
        bus.subscribe(EventType.OBSERVATION, my_handler)
        bus.publish(AgentEvent(event_type=EventType.OBSERVATION, data={...}))
    """

    _instance: Optional['AgentEventBus'] = None
    _lock = threading.Lock()

    def __init__(self):
        # Subscribers: event_type → list of handlers
        self._subscribers: Dict[EventType, List[EventHandler]] = defaultdict(list)
        # Global subscribers that receive ALL events
        self._global_subscribers: List[EventHandler] = []
        # Recent event history (ring buffer)
        self._recent_events: List[AgentEvent] = []
        self._max_recent = 1000
        # Statistics
        self._event_counts: Dict[EventType, int] = defaultdict(int)
        # Thread safety
        self._pubsub_lock = threading.Lock()
        self._initialized = True
        logger.info("AgentEventBus initialized")

    @classmethod
    def get_instance(cls) -> 'AgentEventBus':
        """Get the singleton instance of the event bus."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing only)."""
        with cls._lock:
            cls._instance = None

    # ── Pub/Sub ─────────────────────────────────────────────────

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Subscribe to a specific event type."""
        with self._pubsub_lock:
            self._subscribers[event_type].append(handler)
            logger.debug(f"Handler subscribed to {event_type.value}")

    def subscribe_all(self, handler: EventHandler) -> None:
        """Subscribe to ALL events (for observability, logging)."""
        with self._pubsub_lock:
            self._global_subscribers.append(handler)
            logger.debug("Global handler subscribed")

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Unsubscribe a handler from an event type."""
        with self._pubsub_lock:
            if handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)

    def unsubscribe_all(self, handler: EventHandler) -> None:
        """Unsubscribe a global handler."""
        with self._pubsub_lock:
            if handler in self._global_subscribers:
                self._global_subscribers.remove(handler)

    def publish(self, event: AgentEvent) -> None:
        """
        Publish an event to all subscribers.

        Handlers are called synchronously in subscription order.
        For async handlers, wrap them in a coroutine dispatcher.
        """
        with self._pubsub_lock:
            self._event_counts[event.event_type] += 1

            # Store in ring buffer
            self._recent_events.append(event)
            if len(self._recent_events) > self._max_recent:
                self._recent_events = self._recent_events[-self._max_recent:]

            # Notify type-specific subscribers
            handlers = list(self._subscribers.get(event.event_type, []))

        # Call handlers outside the lock to prevent deadlocks
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Event handler error for {event.event_type.value}: {e}")

        # Notify global subscribers
        for handler in list(self._global_subscribers):
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Global event handler error: {e}")

    # ── Convenience Publishers ──────────────────────────────────

    def emit_observation(
        self,
        agent_id: str,
        data: Dict[str, Any],
        user_id_hash: Optional[str] = None,
        dialect: Optional[str] = None,
    ) -> None:
        """Emit an observation event."""
        self.publish(AgentEvent(
            event_type=EventType.OBSERVATION,
            agent_id=agent_id,
            user_id_hash=user_id_hash,
            dialect=dialect,
            data=data,
        ))

    def emit_decision(
        self,
        agent_id: str,
        decision: str,
        reasoning: Optional[str] = None,
        user_id_hash: Optional[str] = None,
    ) -> None:
        """Emit a decision event."""
        self.publish(AgentEvent(
            event_type=EventType.DECISION,
            agent_id=agent_id,
            user_id_hash=user_id_hash,
            data={"decision": decision, "reasoning": reasoning},
        ))

    def emit_action_result(
        self,
        agent_id: str,
        action: str,
        success: bool,
        result: Any = None,
        error: Optional[str] = None,
        user_id_hash: Optional[str] = None,
    ) -> None:
        """Emit an action result event."""
        self.publish(AgentEvent(
            event_type=EventType.ACTION_RESULT,
            agent_id=agent_id,
            user_id_hash=user_id_hash,
            data={
                "action": action,
                "success": success,
                "result": result,
                "error": error,
            },
        ))

    def emit_reflection(
        self,
        agent_id: str,
        reflection: str,
        lessons: Optional[List[str]] = None,
        user_id_hash: Optional[str] = None,
    ) -> None:
        """Emit a reflection event."""
        self.publish(AgentEvent(
            event_type=EventType.REFLECTION,
            agent_id=agent_id,
            user_id_hash=user_id_hash,
            data={"reflection": reflection, "lessons": lessons or []},
        ))

    def emit_memory_recall(
        self,
        agent_id: str,
        data: Dict[str, Any],
    ) -> None:
        """Emit a memory recall event for observability."""
        self.publish(AgentEvent(
            event_type=EventType.MEMORY_RECALL,
            agent_id=agent_id,
            data=data,
        ))

    def emit_memory_store(
        self,
        agent_id: str,
        tier: str,
        data: Dict[str, Any],
    ) -> None:
        """Emit a memory store event for observability."""
        self.publish(AgentEvent(
            event_type=EventType.MEMORY_STORE,
            agent_id=agent_id,
            data={"tier": tier, **data},
        ))

    # ── Queries ─────────────────────────────────────────────────

    def get_recent_events(
        self,
        event_type: Optional[EventType] = None,
        limit: int = 50,
    ) -> List[AgentEvent]:
        """Get recent events, optionally filtered by type."""
        if event_type:
            return [e for e in self._recent_events if e.event_type == event_type][-limit:]
        return self._recent_events[-limit:]

    def get_event_stats(self) -> Dict[str, int]:
        """Get event count statistics."""
        return {k.value: v for k, v in self._event_counts.items()}

    def clear_history(self) -> None:
        """Clear event history (for testing)."""
        with self._pubsub_lock:
            self._recent_events.clear()
            self._event_counts.clear()

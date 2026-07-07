"""
Three-Tier Memory System for Msaidizi Agents
=============================================

Implements the memory architecture recommended by Swarm 3 research:
  Working Memory → Episodic Memory → LongTerm Memory

Memory tiers:
1. Working Memory (short-term, current context)
   - Current conversation context
   - Priority-weighted eviction with exponential decay
   - Capacity: ~50 items

2. Episodic Memory (medium-term, past interactions)
   - Past interactions with similarity-based retrieval
   - Lesson extraction from successes and failures
   - Failure pattern analysis
   - Capacity: ~1000 items with decay

3. LongTerm Memory (long-term, distilled patterns)
   - Distilled patterns with confidence scoring
   - Reinforcement from repeated observations
   - Decay for outdated patterns
   - Capacity: ~500 patterns

The memory system subscribes to the AgentEventBus and automatically
stores observations, decisions, and reflections. Agents interact with
memory through the TieredMemoryManager, which provides the
observe→think→act→reflect flow.

Integration with AgentEventBus:
  - All memory operations emit events for observability
  - Memory consolidation is triggered by events
  - Agents are notified of memory changes via the bus

@author Angavu Intelligence — Fix Swarm 3 (Memory System Wiring)
"""

from __future__ import annotations

import hashlib
import logging
import math
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from ..event_bus import AgentEventBus, AgentEvent, EventType

logger = logging.getLogger(__name__)


# ── Pattern Types ───────────────────────────────────────────────

class PatternType(Enum):
    """Types of patterns stored in long-term memory."""
    PREFERENCE = "preference"         # User preferences (language, timing)
    RULE = "rule"                     # Learned business rules
    TREND = "trend"                   # Market/business trends
    CORRELATION = "correlation"       # Correlated events
    BEHAVIOR = "behavior"             # User behavior patterns
    FAILURE = "failure"               # Known failure patterns
    SUCCESS = "success"               # Successful strategies


# ── Working Memory ──────────────────────────────────────────────

@dataclass
class MemoryItem:
    """An item in working memory."""
    content: Any
    priority: float = 1.0
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    item_type: str = "observation"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def effective_priority(self) -> float:
        """Priority with exponential decay over time."""
        age_minutes = (time.time() - self.timestamp) / 60
        decay = math.exp(-age_minutes / 30)  # 30-minute half-life
        return self.priority * decay


class WorkingMemory:
    """
    Short-term memory for current context.

    Stores the current conversation context, recent observations,
    and active goals. Uses priority-weighted eviction with
    exponential decay to manage capacity.

    Capacity: ~50 items (configurable)
    """

    def __init__(self, capacity: int = 50):
        self.capacity = capacity
        self._items: List[MemoryItem] = []
        self._context: Dict[str, Any] = {}

    def store(self, item: MemoryItem) -> None:
        """Store an item, evicting lowest-priority if at capacity."""
        self._items.append(item)
        if len(self._items) > self.capacity:
            self._evict()

    def store_interaction(self, user_input: str, agent_response: str, dialect: str) -> None:
        """Store a conversation turn."""
        self.store(MemoryItem(
            content={"user": user_input, "agent": agent_response},
            priority=0.8,
            source="conversation",
            item_type="interaction",
            metadata={"dialect": dialect},
        ))

    def store_observation(self, observation: Any, priority: float = 0.6) -> None:
        """Store an observation."""
        self.store(MemoryItem(
            content=observation,
            priority=priority,
            source="observation",
            item_type="observation",
        ))

    def recall_recent(self, limit: int = 10) -> List[MemoryItem]:
        """Get the most recent items."""
        return sorted(self._items, key=lambda i: i.timestamp, reverse=True)[:limit]

    def recall_by_priority(self, limit: int = 10) -> List[MemoryItem]:
        """Get the highest-priority items (with decay)."""
        return sorted(self._items, key=lambda i: i.effective_priority, reverse=True)[:limit]

    def get_context(self) -> Dict[str, Any]:
        """Get the current context summary."""
        recent = self.recall_recent(5)
        self._context["recent_items"] = [i.content for i in recent]
        self._context["item_count"] = len(self._items)
        return dict(self._context)

    def set_context(self, key: str, value: Any) -> None:
        """Set a context value (e.g., current dialect, user preferences)."""
        self._context[key] = value

    def clear(self) -> None:
        """Clear all working memory."""
        self._items.clear()
        self._context.clear()

    def _evict(self) -> None:
        """Evict the lowest effective-priority item."""
        if not self._items:
            return
        self._items.sort(key=lambda i: i.effective_priority)
        self._items.pop(0)

    def __len__(self) -> int:
        return len(self._items)


# ── Episodic Memory ─────────────────────────────────────────────

@dataclass
class Episode:
    """An episode in episodic memory — a past interaction or event."""
    episode_id: str
    content: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    user_id_hash: Optional[str] = None
    dialect: Optional[str] = None
    outcome: str = "neutral"  # "success", "failure", "neutral"
    lessons: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None  # For similarity search
    access_count: int = 0
    last_accessed: float = 0.0

    @property
    def recency_score(self) -> float:
        """Score based on how recent this episode is."""
        age_hours = (time.time() - self.timestamp) / 3600
        return math.exp(-age_hours / 168)  # 1-week half-life


class EpisodicMemory:
    """
    Medium-term memory for past interactions.

    Stores past episodes with similarity-based retrieval,
    lesson extraction, and failure pattern analysis.

    Capacity: ~1000 episodes with recency decay
    """

    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._episodes: Dict[str, Episode] = {}
        self._failure_patterns: List[Dict[str, Any]] = []
        self._success_patterns: List[Dict[str, Any]] = []

    def store_episode(self, episode: Episode) -> None:
        """Store an episode."""
        self._episodes[episode.episode_id] = episode

        # Extract patterns from outcomes
        if episode.outcome == "failure":
            self._failure_patterns.append({
                "pattern": episode.content,
                "lessons": episode.lessons,
                "timestamp": episode.timestamp,
            })
        elif episode.outcome == "success":
            self._success_patterns.append({
                "pattern": episode.content,
                "lessons": episode.lessons,
                "timestamp": episode.timestamp,
            })

        # Evict old episodes if over capacity
        if len(self._episodes) > self.capacity:
            self._evict()

    def store_interaction(
        self,
        user_input: str,
        agent_response: str,
        user_id_hash: str,
        dialect: str,
        outcome: str = "neutral",
    ) -> str:
        """Store a conversation as an episode."""
        episode_id = hashlib.sha256(
            f"{user_id_hash}:{time.time()}".encode()
        ).hexdigest()[:16]

        episode = Episode(
            episode_id=episode_id,
            content={
                "user_input": user_input,
                "agent_response": agent_response,
            },
            user_id_hash=user_id_hash,
            dialect=dialect,
            outcome=outcome,
        )
        self.store_episode(episode)
        return episode_id

    def recall_similar(
        self,
        query: str,
        limit: int = 5,
        user_id_hash: Optional[str] = None,
    ) -> List[Episode]:
        """
        Recall episodes similar to a query.

        Uses simple keyword overlap for similarity (in production,
        would use embedding-based similarity).
        """
        query_words = set(query.lower().split())
        scored: List[Tuple[float, Episode]] = []

        for ep in self._episodes.values():
            # Filter by user if specified
            if user_id_hash and ep.user_id_hash != user_id_hash:
                continue

            # Simple keyword similarity
            content_str = str(ep.content).lower()
            content_words = set(content_str.split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                similarity = overlap / max(len(query_words), 1)
                # Combine with recency
                score = similarity * 0.7 + ep.recency_score * 0.3
                scored.append((score, ep))

        scored.sort(key=lambda x: x[0], reverse=True)

        # Update access counts
        for _, ep in scored[:limit]:
            ep.access_count += 1
            ep.last_accessed = time.time()

        return [ep for _, ep in scored[:limit]]

    def get_failure_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent failure patterns for learning."""
        return sorted(
            self._failure_patterns,
            key=lambda p: p["timestamp"],
            reverse=True
        )[:limit]

    def get_success_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent success patterns for reinforcement."""
        return sorted(
            self._success_patterns,
            key=lambda p: p["timestamp"],
            reverse=True
        )[:limit]

    def _evict(self) -> None:
        """Evict the oldest, least-accessed episode."""
        if not self._episodes:
            return
        # Sort by access count (ascending) then recency (ascending)
        sorted_eps = sorted(
            self._episodes.values(),
            key=lambda e: (e.access_count, e.recency_score)
        )
        if sorted_eps:
            del self._episodes[sorted_eps[0].episode_id]

    def __len__(self) -> int:
        return len(self._episodes)


# ── Long-Term Memory ────────────────────────────────────────────

@dataclass
class Pattern:
    """A distilled pattern in long-term memory."""
    pattern_id: str
    pattern_type: PatternType
    description: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.5
    reinforcement_count: int = 0
    last_reinforced: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def reinforce(self, amount: float = 0.1) -> None:
        """Reinforce this pattern (increase confidence)."""
        self.confidence = min(1.0, self.confidence + amount)
        self.reinforcement_count += 1
        self.last_reinforced = time.time()

    def decay(self, amount: float = 0.01) -> None:
        """Decay this pattern (decrease confidence over time)."""
        self.confidence = max(0.0, self.confidence - amount)

    @property
    def is_stale(self) -> bool:
        """Whether this pattern hasn't been reinforced recently."""
        age_days = (time.time() - self.last_reinforced) / 86400
        return age_days > 30  # Stale after 30 days without reinforcement

    @property
    def effective_confidence(self) -> float:
        """Confidence adjusted for staleness."""
        if self.is_stale:
            age_days = (time.time() - self.last_reinforced) / 86400
            decay = math.exp(-age_days / 60)  # 60-day half-life
            return self.confidence * decay
        return self.confidence


class LongTermMemory:
    """
    Long-term memory for distilled patterns.

    Stores patterns with confidence scoring, reinforcement,
    and decay. Patterns are distilled from episodic memory
    during consolidation.

    Capacity: ~500 patterns
    """

    def __init__(self, capacity: int = 500):
        self.capacity = capacity
        self._patterns: Dict[str, Pattern] = {}

    def store_pattern(self, pattern: Pattern) -> None:
        """Store a new pattern."""
        # Check if similar pattern exists — reinforce instead
        existing = self._find_similar(pattern)
        if existing:
            existing.reinforce(0.1)
            existing.evidence.extend(pattern.evidence[:3])
            return

        self._patterns[pattern.pattern_id] = pattern

        if len(self._patterns) > self.capacity:
            self._evict()

    def store_user_preference(
        self,
        user_id_hash: str,
        preference: str,
        value: Any,
        confidence: float = 0.6,
    ) -> None:
        """Store a user preference pattern."""
        pattern_id = f"pref_{user_id_hash}_{hashlib.md5(preference.encode()).hexdigest()[:8]}"
        self.store_pattern(Pattern(
            pattern_id=pattern_id,
            pattern_type=PatternType.PREFERENCE,
            description=f"User {user_id_hash[:8]} prefers {preference}={value}",
            evidence=[f"Observed at {time.time()}"],
            confidence=confidence,
            metadata={"user_id_hash": user_id_hash, "preference": preference, "value": value},
        ))

    def store_business_rule(
        self,
        rule: str,
        evidence: str,
        confidence: float = 0.7,
    ) -> None:
        """Store a learned business rule."""
        pattern_id = f"rule_{hashlib.md5(rule.encode()).hexdigest()[:12]}"
        self.store_pattern(Pattern(
            pattern_id=pattern_id,
            pattern_type=PatternType.RULE,
            description=rule,
            evidence=[evidence],
            confidence=confidence,
        ))

    def recall_by_type(
        self,
        pattern_type: PatternType,
        min_confidence: float = 0.3,
        limit: int = 20,
    ) -> List[Pattern]:
        """Recall patterns of a specific type above confidence threshold."""
        matching = [
            p for p in self._patterns.values()
            if p.pattern_type == pattern_type
            and p.effective_confidence >= min_confidence
        ]
        matching.sort(key=lambda p: p.effective_confidence, reverse=True)
        return matching[:limit]

    def recall_for_user(
        self,
        user_id_hash: str,
        limit: int = 10,
    ) -> List[Pattern]:
        """Recall patterns relevant to a specific user."""
        matching = [
            p for p in self._patterns.values()
            if p.metadata.get("user_id_hash") == user_id_hash
        ]
        matching.sort(key=lambda p: p.effective_confidence, reverse=True)
        return matching[:limit]

    def run_decay(self, decay_amount: float = 0.005) -> int:
        """
        Apply decay to all patterns. Returns count of removed patterns.

        Called periodically during memory consolidation.
        """
        to_remove = []
        for pid, pattern in self._patterns.items():
            pattern.decay(decay_amount)
            if pattern.effective_confidence < 0.05:
                to_remove.append(pid)

        for pid in to_remove:
            del self._patterns[pid]

        return len(to_remove)

    def _find_similar(self, pattern: Pattern) -> Optional[Pattern]:
        """Find an existing similar pattern."""
        for existing in self._patterns.values():
            if (existing.pattern_type == pattern.pattern_type
                    and existing.description == pattern.description):
                return existing
            # Check metadata match for preferences
            if (pattern.pattern_type == PatternType.PREFERENCE
                    and existing.metadata.get("user_id_hash") == pattern.metadata.get("user_id_hash")
                    and existing.metadata.get("preference") == pattern.metadata.get("preference")):
                return existing
        return None

    def _evict(self) -> None:
        """Evict the lowest-confidence stale pattern."""
        stale = [p for p in self._patterns.values() if p.is_stale]
        if stale:
            stale.sort(key=lambda p: p.effective_confidence)
            del self._patterns[stale[0].pattern_id]
        elif self._patterns:
            # If nothing is stale, evict lowest confidence
            lowest = min(self._patterns.values(), key=lambda p: p.effective_confidence)
            del self._patterns[lowest.pattern_id]

    def __len__(self) -> int:
        return len(self._patterns)


# ── Tiered Memory Manager ──────────────────────────────────────

class TieredMemoryManager:
    """
    Unified memory manager that connects all three tiers.

    Implements the observe→think→act→reflect flow:
    1. Observe: Store incoming observations in working memory
    2. Think: Retrieve relevant memories from all tiers
    3. Act: Execute action based on context
    4. Reflect: Store outcome, extract lessons, consolidate

    Integrates with AgentEventBus for automatic event-driven
    memory operations and observability.
    """

    def __init__(self, agent_id: str, event_bus: Optional[AgentEventBus] = None):
        self.agent_id = agent_id
        self.event_bus = event_bus or AgentEventBus.get_instance()

        # Three tiers
        self.working = WorkingMemory(capacity=50)
        self.episodic = EpisodicMemory(capacity=1000)
        self.long_term = LongTermMemory(capacity=500)

        # Consolidation state
        self._last_consolidation = time.time()
        self._consolidation_interval = 3600  # 1 hour

        # Wire up event bus subscriptions
        self._subscribe_to_events()

        logger.info(f"TieredMemoryManager initialized for agent {agent_id}")

    def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events on the bus."""
        self.event_bus.subscribe(EventType.OBSERVATION, self._on_observation)
        self.event_bus.subscribe(EventType.ACTION_RESULT, self._on_action_result)
        self.event_bus.subscribe(EventType.REFLECTION, self._on_reflection)
        self.event_bus.subscribe(EventType.INTERACTION_END, self._on_interaction_end)
        logger.debug(f"Agent {self.agent_id} memory subscribed to event bus")

    # ── Observe ─────────────────────────────────────────────────

    def observe(self, observation: Any, priority: float = 0.6) -> None:
        """
        Store an observation in working memory and emit event.
        """
        self.working.store_observation(observation, priority)
        self.event_bus.emit_observation(
            agent_id=self.agent_id,
            data={"observation": observation, "priority": priority},
        )

    def observe_interaction(
        self,
        user_input: str,
        agent_response: str,
        user_id_hash: str,
        dialect: str,
    ) -> None:
        """Store a conversation turn in working memory."""
        self.working.store_interaction(user_input, agent_response, dialect)
        # Also store in episodic memory
        self.episodic.store_interaction(
            user_input, agent_response, user_id_hash, dialect
        )

    # ── Think (Retrieve) ────────────────────────────────────────

    def think(self, query: str, user_id_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve relevant memories from all tiers for a query.

        Returns a context dict with:
        - working_context: Current conversation context
        - similar_episodes: Past similar interactions
        - relevant_patterns: Long-term patterns that apply
        - failure_warnings: Known failure patterns to avoid
        """
        # Working memory context
        working_context = self.working.get_context()

        # Episodic recall
        similar_episodes = self.episodic.recall_similar(query, limit=5, user_id_hash=user_id_hash)

        # Long-term pattern recall
        relevant_patterns = []
        if user_id_hash:
            relevant_patterns = self.long_term.recall_for_user(user_id_hash, limit=5)

        # Failure pattern warnings
        failure_warnings = self.episodic.get_failure_patterns(limit=3)

        self.event_bus.emit_memory_recall(
            agent_id=self.agent_id,
            data={"query": query, "episodes_found": len(similar_episodes)},
        ) if hasattr(self.event_bus, 'emit_memory_recall') else None

        return {
            "working_context": working_context,
            "similar_episodes": [
                {"content": ep.content, "outcome": ep.outcome, "lessons": ep.lessons}
                for ep in similar_episodes
            ],
            "relevant_patterns": [
                {"description": p.description, "confidence": p.effective_confidence, "type": p.pattern_type.value}
                for p in relevant_patterns
            ],
            "failure_warnings": failure_warnings,
        }

    # ── Reflect ─────────────────────────────────────────────────

    def reflect(
        self,
        action: str,
        outcome: str,
        lessons: Optional[List[str]] = None,
        user_id_hash: Optional[str] = None,
    ) -> None:
        """
        Reflect on an action's outcome. Stores in episodic and
        distills patterns for long-term memory.
        """
        # Store in episodic memory as an episode
        episode_id = hashlib.sha256(
            f"{self.agent_id}:{action}:{time.time()}".encode()
        ).hexdigest()[:16]

        self.episodic.store_episode(Episode(
            episode_id=episode_id,
            content={"action": action, "outcome": outcome},
            outcome="success" if "success" in outcome.lower() else "failure" if "fail" in outcome.lower() else "neutral",
            lessons=lessons or [],
            user_id_hash=user_id_hash,
        ))

        # Emit reflection event
        self.event_bus.emit_reflection(
            agent_id=self.agent_id,
            reflection=f"Action '{action}' resulted in: {outcome}",
            lessons=lessons,
            user_id_hash=user_id_hash,
        )

        # Periodically consolidate
        self._maybe_consolidate()

    # ── Consolidation ───────────────────────────────────────────

    def consolidate(self) -> Dict[str, int]:
        """
        Run memory consolidation:
        1. Decay old long-term patterns
        2. Distill frequent episodic patterns into long-term
        3. Clean up stale entries

        Returns consolidation stats.
        """
        now = time.time()
        self._last_consolidation = now

        # Decay long-term patterns
        removed = self.long_term.run_decay()

        # Distill from episodic → long-term
        distilled = self._distill_patterns()

        stats = {
            "patterns_decayed": removed,
            "patterns_distilled": distilled,
            "working_memory_size": len(self.working),
            "episodic_memory_size": len(self.episodic),
            "long_term_memory_size": len(self.long_term),
        }

        self.event_bus.publish(AgentEvent(
            event_type=EventType.MEMORY_CONSOLIDATION,
            agent_id=self.agent_id,
            data=stats,
        ))

        logger.info(f"Memory consolidation complete for agent {self.agent_id}: {stats}")
        return stats

    def _distill_patterns(self) -> int:
        """Distill frequent patterns from episodic to long-term memory."""
        distilled = 0

        # Distill success patterns
        for sp in self.episodic.get_success_patterns(limit=5):
            if sp.get("lessons"):
                self.long_term.store_pattern(Pattern(
                    pattern_id=f"distilled_{hashlib.md5(str(sp['pattern']).encode()).hexdigest()[:12]}",
                    pattern_type=PatternType.SUCCESS,
                    description=str(sp["pattern"])[:200],
                    evidence=sp["lessons"][:3],
                    confidence=0.6,
                ))
                distilled += 1

        return distilled

    def _maybe_consolidate(self) -> None:
        """Run consolidation if enough time has passed."""
        if time.time() - self._last_consolidation > self._consolidation_interval:
            self.consolidate()

    # ── Event Handlers ──────────────────────────────────────────

    def _on_observation(self, event: AgentEvent) -> None:
        """Handle observation events from the bus."""
        observation = event.data.get("observation")
        if observation and event.agent_id != self.agent_id:
            # Store observations from other agents in working memory
            self.working.store(MemoryItem(
                content=observation,
                priority=0.4,
                source=f"agent:{event.agent_id}",
                item_type="cross_agent_observation",
            ))

    def _on_action_result(self, event: AgentEvent) -> None:
        """Handle action result events."""
        if event.agent_id != self.agent_id:
            return
        success = event.data.get("success", False)
        action = event.data.get("action", "unknown")
        if not success:
            # Store failure in working memory with high priority
            self.working.store(MemoryItem(
                content={"failed_action": action, "error": event.data.get("error")},
                priority=1.0,
                source="action_failure",
                item_type="failure",
            ))

    def _on_reflection(self, event: AgentEvent) -> None:
        """Handle reflection events — update long-term patterns."""
        if event.agent_id != self.agent_id:
            return
        lessons = event.data.get("lessons", [])
        if lessons:
            for lesson in lessons:
                self.long_term.store_business_rule(
                    rule=lesson,
                    evidence=f"Reflected by agent {self.agent_id}",
                    confidence=0.5,
                )

    def _on_interaction_end(self, event: AgentEvent) -> None:
        """Handle interaction end — store and potentially consolidate."""
        user_id_hash = event.user_id_hash
        if user_id_hash:
            # Store user interaction pattern
            self.long_term.store_user_preference(
                user_id_hash=user_id_hash,
                preference="last_interaction_time",
                value=event.timestamp,
                confidence=0.8,
            )

    # ── API for agents ──────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics."""
        return {
            "agent_id": self.agent_id,
            "working_memory": len(self.working),
            "episodic_memory": len(self.episodic),
            "long_term_memory": len(self.long_term),
            "last_consolidation": self._last_consolidation,
            "event_bus_stats": self.event_bus.get_event_stats(),
        }

    def clear_working(self) -> None:
        """Clear working memory (e.g., new conversation)."""
        self.working.clear()

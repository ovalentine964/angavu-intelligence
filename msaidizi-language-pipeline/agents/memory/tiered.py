"""
Three-Layer Memory System for Msaidizi Agents
==============================================

Implements the Hermes three-layer memory architecture adapted for
Msaidizi's 33-agent system serving 600M+ informal workers.

Architecture (Hermes Pattern → Angavu Adaptation):
  L1 (Session)    → Working Memory — in-process conversation buffer
  L2 (Episodic)   → Episodic Memory — SQLite + FTS5 full-text search
  L3 (User Model) → Long-Term Memory — Bayesian behavioral model

Key improvements over Swarm 3 baseline:
  - SQLite FTS5 for sub-10ms full-text search of episodic memory
  - Bayesian updating (STA 142) for the L3 worker behavioral model
  - Predictive model: what will this worker need next?
  - Closed learning loop: auto-generate skills from complex tasks

Academic basis:
  - STA 142 (Probability): Bayesian updating for worker model
  - ECO 201 (Producer Theory): Learn from production decisions
  - STA 142 (Statistical Learning): FTS5 BM25 for retrieval
  - Hermes Architecture: Three-layer memory with closed learning loop

Memory tiers:
1. Working Memory (L1 — Session Context)
   - Current conversation context
   - Priority-weighted eviction with exponential decay
   - Capacity: ~50 items
   - Lifetime: session only

2. Episodic Memory (L2 — SQLite + FTS5)
   - Past interactions stored in SQLite with FTS5 full-text index
   - Sub-10ms retrieval for on-device queries
   - Stores: worker queries, responses, outcomes, timestamps
   - Capacity: ~10,000 episodes with relevance decay
   - Lifetime: permanent (on-device)

3. Long-Term Memory (L3 — User Model)
   - Worker behavioral model: decision patterns, risk tolerance
   - Bayesian updating with each interaction
   - Predictive model: anticipate worker needs
   - Capacity: ~500 patterns per worker
   - Lifetime: permanent, drift-adjusted

The memory system subscribes to the AgentEventBus and automatically
stores observations, decisions, and reflections. Agents interact with
memory through the TieredMemoryManager, which provides the
observe→think→act→reflect flow.

Integration with AgentEventBus:
  - All memory operations emit events for observability
  - Memory consolidation is triggered by events
  - Agents are notified of memory changes via the bus

@author Angavu Intelligence — Implementation Swarm 14 (Hermes Memory)
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import sqlite3
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
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


# ── SQLite FTS5 Episodic Store (L2) ─────────────────────────────


class SQLiteFTS5Store:
    """
    SQLite + FTS5 backend for episodic memory.

    Implements Hermes's L2 pattern: persistent, searchable episodic store
    with sub-10ms retrieval on 10K+ episodes.

    Why SQLite FTS5:
      - Zero dependencies (Python stdlib)
      - Sub-10ms full-text search with BM25 ranking
      - Works fully offline (critical for Africa's connectivity gaps)
      - Handles Swahili/multilingual text via unicode61 tokenizer
      - No embedding model needed (saves memory on constrained devices)

    Academic basis:
      - STA 142: BM25 is a probabilistic retrieval model
      - ECO 201: Store production decisions for pattern learning
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = Path(os.environ.get(
                "MSAIDIZI_DATA_DIR",
                Path.home() / ".msaidizi" / "memory"
            ))
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "episodic.db")

        self._db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()
        logger.info(f"SQLite FTS5 episodic store initialized at {db_path}")

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.execute("PRAGMA cache_size=-8000")  # 8MB cache
        return self._conn

    def _init_db(self) -> None:
        conn = self._get_conn()

        # Main episodes table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                episode_id TEXT PRIMARY KEY,
                worker_id TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                outcome TEXT NOT NULL DEFAULT 'neutral',
                lessons TEXT DEFAULT '[]',
                dialect TEXT DEFAULT '',
                business_context TEXT DEFAULT '{}',
                timestamp INTEGER NOT NULL,
                access_count INTEGER DEFAULT 0,
                relevance_boost REAL DEFAULT 1.0
            )
        """)

        # FTS5 virtual table for full-text search
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS episodes_fts USING fts5(
                query, response, lessons, business_context,
                content='episodes', content_rowid='rowid',
                tokenize='unicode61 remove_diacritics 2'
            )
        """)

        # Triggers for FTS sync
        for trigger_sql in [
            """CREATE TRIGGER IF NOT EXISTS episodes_ai AFTER INSERT ON episodes BEGIN
                INSERT INTO episodes_fts(rowid, query, response, lessons, business_context)
                VALUES (new.rowid, new.query, new.response, new.lessons, new.business_context);
            END""",
            """CREATE TRIGGER IF NOT EXISTS episodes_ad AFTER DELETE ON episodes BEGIN
                INSERT INTO episodes_fts(episodes_fts, rowid, query, response, lessons, business_context)
                VALUES ('delete', old.rowid, old.query, old.response, old.lessons, old.business_context);
            END""",
            """CREATE TRIGGER IF NOT EXISTS episodes_au AFTER UPDATE ON episodes BEGIN
                INSERT INTO episodes_fts(episodes_fts, rowid, query, response, lessons, business_context)
                VALUES ('delete', old.rowid, old.query, old.response, old.lessons, old.business_context);
                INSERT INTO episodes_fts(rowid, query, response, lessons, business_context)
                VALUES (new.rowid, new.query, new.response, new.lessons, new.business_context);
            END""",
        ]:
            conn.execute(trigger_sql)

        # Indexes for fast retrieval
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_ep_worker "
            "ON episodes(worker_id, timestamp DESC)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_ep_outcome "
            "ON episodes(outcome, timestamp DESC)"
        )

        # Skills table for the closed learning loop
        conn.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                skill_id TEXT PRIMARY KEY,
                worker_id TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                source_episode_id TEXT,
                confidence REAL DEFAULT 0.5,
                business_context TEXT DEFAULT '{}',
                timestamp INTEGER NOT NULL,
                access_count INTEGER DEFAULT 0
            )
        """)

        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
                title, body,
                content='skills', content_rowid='rowid',
                tokenize='unicode61 remove_diacritics 2'
            )
        """)

        conn.execute("""CREATE TRIGGER IF NOT EXISTS skills_ai AFTER INSERT ON skills BEGIN
            INSERT INTO skills_fts(rowid, title, body)
            VALUES (new.rowid, new.title, new.body);
        END""")

        conn.execute("""CREATE TRIGGER IF NOT EXISTS skills_ad AFTER DELETE ON skills BEGIN
            INSERT INTO skills_fts(skills_fts, rowid, title, body)
            VALUES ('delete', old.rowid, old.title, old.body);
        END""")

        conn.commit()

    def store_episode(
        self,
        episode_id: str,
        worker_id: str,
        query: str,
        response: str,
        outcome: str = "neutral",
        lessons: Optional[List[str]] = None,
        dialect: str = "",
        business_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store an episode in SQLite with FTS5 indexing."""
        conn = self._get_conn()
        conn.execute(
            """INSERT OR REPLACE INTO episodes
            (episode_id, worker_id, query, response, outcome, lessons,
             dialect, business_context, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                episode_id, worker_id, query, response, outcome,
                json.dumps(lessons or []),
                dialect,
                json.dumps(business_context or {}),
                int(time.time() * 1000),
            ),
        )
        conn.commit()

    def search_episodes(
        self,
        query: str,
        worker_id: Optional[str] = None,
        outcome: Optional[str] = None,
        limit: int = 10,
    ) -> List[Episode]:
        """
        Full-text search of episodic memory using FTS5 BM25.

        Target: sub-10ms for 10K+ episodes.
        """
        if not query.strip():
            return []

        conn = self._get_conn()
        fts_query = self._sanitize_fts_query(query)

        sql = """
            SELECT e.episode_id, e.worker_id, e.query, e.response,
                   e.outcome, e.lessons, e.dialect, e.business_context,
                   e.timestamp, e.access_count,
                   bm25(episodes_fts) AS rank
            FROM episodes_fts f
            JOIN episodes e ON e.rowid = f.rowid
            WHERE episodes_fts MATCH ?
        """
        params: List[Any] = [fts_query]

        if worker_id:
            sql += " AND e.worker_id = ?"
            params.append(worker_id)
        if outcome:
            sql += " AND e.outcome = ?"
            params.append(outcome)

        sql += " ORDER BY (bm25(episodes_fts) * e.relevance_boost) ASC LIMIT ?"
        params.append(limit)

        start = time.monotonic_ns()
        rows = conn.execute(sql, params).fetchall()
        elapsed_ms = (time.monotonic_ns() - start) / 1_000_000

        episodes = []
        for row in rows:
            lessons = json.loads(row[5]) if row[5] else []
            ep = Episode(
                episode_id=row[0],
                content={"user_input": row[2], "agent_response": row[3]},
                timestamp=row[8] / 1000.0,
                user_id_hash=row[1],
                dialect=row[6],
                outcome=row[4],
                lessons=lessons,
                access_count=row[9],
            )
            episodes.append(ep)

        # Update access counts
        if episodes:
            ids = [ep.episode_id for ep in episodes]
            placeholders = ",".join("?" * len(ids))
            conn.execute(
                f"UPDATE episodes SET access_count = access_count + 1 "
                f"WHERE episode_id IN ({placeholders})",
                ids,
            )
            conn.commit()

        logger.debug(
            f"FTS5 search '{query[:30]}...' → {len(episodes)} results "
            f"in {elapsed_ms:.2f}ms"
        )
        return episodes

    def store_skill(
        self,
        skill_id: str,
        worker_id: str,
        title: str,
        body: str,
        source_episode_id: Optional[str] = None,
        confidence: float = 0.5,
        business_context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store a generated skill (closed learning loop output)."""
        conn = self._get_conn()
        conn.execute(
            """INSERT OR REPLACE INTO skills
            (skill_id, worker_id, title, body, source_episode_id,
             confidence, business_context, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                skill_id, worker_id, title, body,
                source_episode_id, confidence,
                json.dumps(business_context or {}),
                int(time.time() * 1000),
            ),
        )
        conn.commit()
        logger.info(f"Stored skill '{title}' for worker {worker_id[:8]}...")

    def search_skills(
        self,
        query: str,
        worker_id: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Search skills using FTS5."""
        if not query.strip():
            return []

        conn = self._get_conn()
        fts_query = self._sanitize_fts_query(query)

        sql = """
            SELECT s.skill_id, s.worker_id, s.title, s.body,
                   s.source_episode_id, s.confidence, s.business_context,
                   s.timestamp, bm25(skills_fts) AS rank
            FROM skills_fts f
            JOIN skills s ON s.rowid = f.rowid
            WHERE skills_fts MATCH ?
        """
        params: List[Any] = [fts_query]
        if worker_id:
            sql += " AND s.worker_id = ?"
            params.append(worker_id)
        sql += " ORDER BY (bm25(skills_fts) * s.confidence) ASC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        return [
            {
                "skill_id": r[0], "worker_id": r[1], "title": r[2],
                "body": r[3], "source_episode_id": r[4],
                "confidence": r[5],
                "business_context": json.loads(r[6]) if r[6] else {},
                "timestamp": r[7], "bm25_rank": r[8],
            }
            for r in rows
        ]

    def get_failure_episodes(
        self, worker_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get failure episodes for learning."""
        conn = self._get_conn()
        rows = conn.execute(
            """SELECT episode_id, query, response, lessons, timestamp
            FROM episodes WHERE worker_id = ? AND outcome = 'failure'
            ORDER BY timestamp DESC LIMIT ?""",
            (worker_id, limit),
        ).fetchall()
        return [
            {
                "episode_id": r[0], "query": r[1], "response": r[2],
                "lessons": json.loads(r[3]) if r[3] else [],
                "timestamp": r[4],
            }
            for r in rows
        ]

    def get_success_episodes(
        self, worker_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get success episodes for skill generation."""
        conn = self._get_conn()
        rows = conn.execute(
            """SELECT episode_id, query, response, lessons, business_context, timestamp
            FROM episodes WHERE worker_id = ? AND outcome = 'success'
            ORDER BY timestamp DESC LIMIT ?""",
            (worker_id, limit),
        ).fetchall()
        return [
            {
                "episode_id": r[0], "query": r[1], "response": r[2],
                "lessons": json.loads(r[3]) if r[3] else [],
                "business_context": json.loads(r[4]) if r[4] else {},
                "timestamp": r[5],
            }
            for r in rows
        ]

    def run_decay(self, decay_amount: float = 0.02) -> int:
        """Decay relevance and remove stale episodes. Returns removed count."""
        conn = self._get_conn()
        conn.execute(
            "UPDATE episodes SET relevance_boost = MAX(0.0, relevance_boost - ?)",
            (decay_amount,),
        )
        cutoff = int((time.time() - 30 * 86400) * 1000)  # 30 days
        cursor = conn.execute(
            "DELETE FROM episodes WHERE relevance_boost < 0.1 AND timestamp < ?",
            (cutoff,),
        )
        conn.commit()
        removed = cursor.rowcount
        if removed:
            logger.debug(f"FTS5 decay removed {removed} stale episodes")
        return removed

    def _sanitize_fts_query(self, query: str) -> str:
        """Escape FTS5 special characters and build OR query."""
        cleaned = query.replace('"', "'").replace("*", "").replace("-", " ")
        words = [w for w in cleaned.strip().split() if len(w) > 1]
        if not words:
            return '"' + query.strip() + '"'
        if len(words) == 1:
            return '"' + words[0] + '"'
        return " OR ".join('"' + w + '"' for w in words)

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None


class EpisodicMemory:
    """
    Medium-term memory for past interactions.

    Stores past episodes with similarity-based retrieval,
    lesson extraction, and failure pattern analysis.

    Capacity: ~1000 episodes with recency decay
    """

    def __init__(self, capacity: int = 1000, sqlite_store: Optional[SQLiteFTS5Store] = None):
        self.capacity = capacity
        self._episodes: Dict[str, Episode] = {}
        self._failure_patterns: List[Dict[str, Any]] = []
        self._success_patterns: List[Dict[str, Any]] = []
        self._sqlite_store = sqlite_store  # L2 FTS5 backend

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
        lessons: Optional[List[str]] = None,
        business_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Store a conversation as an episode in both memory and SQLite."""
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
            lessons=lessons or [],
        )
        self.store_episode(episode)

        # Also persist to SQLite FTS5 for fast retrieval
        if self._sqlite_store:
            self._sqlite_store.store_episode(
                episode_id=episode_id,
                worker_id=user_id_hash,
                query=user_input,
                response=agent_response,
                outcome=outcome,
                lessons=lessons or [],
                dialect=dialect,
                business_context=business_context or {},
            )

        return episode_id

    def recall_similar(
        self,
        query: str,
        limit: int = 5,
        user_id_hash: Optional[str] = None,
    ) -> List[Episode]:
        """
        Recall episodes similar to a query.

        Uses FTS5 BM25 ranking when available, falls back to
        keyword overlap for in-memory-only mode.

        Target: sub-10ms for 10K+ episodes on SQLite.
        """
        # Try SQLite FTS5 search first (sub-10ms)
        if self._sqlite_store:
            return self._sqlite_store.search_episodes(
                query=query,
                worker_id=user_id_hash,
                limit=limit,
            )

        # Fallback: in-memory keyword overlap
        query_words = set(query.lower().split())
        scored: List[Tuple[float, Episode]] = []

        for ep in self._episodes.values():
            if user_id_hash and ep.user_id_hash != user_id_hash:
                continue

            content_str = str(ep.content).lower()
            content_words = set(content_str.split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                similarity = overlap / max(len(query_words), 1)
                score = similarity * 0.7 + ep.recency_score * 0.3
                scored.append((score, ep))

        scored.sort(key=lambda x: x[0], reverse=True)

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


# ── L3 User Model: Worker Behavioral Model (Bayesian) ──────────


@dataclass
class WorkerBelief:
    """
    A single Bayesian belief about a worker.

    STA 142 (Probability): Each belief has a mean (expected value),
    variance (uncertainty), and confidence (how much data supports it).

    Updated via conjugate normal Bayesian updating:
      posterior_mean = (prior_mean/prior_var + obs/obs_var) / (1/prior_var + 1/obs_var)
      posterior_var = 1 / (1/prior_var + 1/obs_var)
    """
    name: str
    mean: float
    variance: float
    confidence: float = 0.3  # How much data supports this belief
    update_count: int = 0
    last_updated: float = field(default_factory=time.time)

    def update(self, observation: float, obs_confidence: float = 0.5) -> None:
        """Bayesian update with a new observation."""
        obs_variance = 1.0 / max(obs_confidence * 10, 0.1)
        posterior_var = 1.0 / (1.0 / max(self.variance, 0.001) + 1.0 / obs_variance)
        self.mean = posterior_var * (self.mean / max(self.variance, 0.001) + observation / obs_variance)
        self.variance = posterior_var
        self.confidence = min(1.0, self.confidence + 0.05)
        self.update_count += 1
        self.last_updated = time.time()

    @property
    def effective_confidence(self) -> float:
        """Confidence decayed by staleness."""
        age_days = (time.time() - self.last_updated) / 86400
        if age_days > 30:
            return self.confidence * math.exp(-age_days / 60)
        return self.confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "mean": self.mean, "variance": self.variance,
            "confidence": self.confidence, "update_count": self.update_count,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "WorkerBelief":
        return cls(**d)


class WorkerBehavioralModel:
    """
    L3 User Model — long-term learned behavioral patterns.

    Implements Hermes's L3 pattern: a worker's behavioral model
    that drift-adjusts across sessions using Bayesian updating.

    Tracks:
      - Decision patterns (pricing, restocking, supplier choices)
      - Risk tolerance (willingness to try new products/markets)
      - Preferences (communication style, timing, language)
      - Business patterns (seasonal trends, customer behavior)
      - Predictive signals (what will this worker need next?)

    Academic basis:
      - STA 142: Bayesian updating for all beliefs
      - ECO 201 (Producer Theory): Learn from production decisions
      - ECO 101 (Consumer Theory): Understand substitution patterns
      - ECO 206 (Microfinance): Credit constraints, savings behavior

    Each worker has their own model, stored as JSON in SQLite.
    """

    # Default priors for a new informal worker (ECO 204: African Development)
    DEFAULT_BELIEFS: Dict[str, Tuple[float, float]] = {
        # (mean, variance) — high variance = high uncertainty
        "daily_revenue": (700.0, 500.0),        # KES
        "daily_cost": (400.0, 300.0),           # KES
        "profit_margin": (0.25, 0.15),          # 25% ± 15%
        "savings_rate": (0.05, 0.05),           # 5%
        "risk_aversion": (0.6, 0.2),            # Moderately risk-averse
        "price_sensitivity": (0.8, 0.15),       # High — budget-constrained
        "decision_speed": (0.5, 0.3),           # How fast they decide
        "restock_frequency_days": (3.0, 2.0),   # Days between restocks
        "preferred_early_morning": (0.5, 0.3),  # Whether they prefer early hours
        "loyalty_to_supplier": (0.4, 0.2),      # Supplier stickiness
    }

    def __init__(self, worker_id: str, db_path: Optional[str] = None):
        self.worker_id = worker_id
        self.beliefs: Dict[str, WorkerBelief] = {}
        self.preferences: Dict[str, Any] = {}  # Non-numeric preferences
        self.interaction_history: List[Dict[str, Any]] = []  # Last N interactions for prediction

        # SQLite persistence
        if db_path is None:
            db_dir = Path(os.environ.get(
                "MSAIDIZI_DATA_DIR",
                Path.home() / ".msaidizi" / "memory"
            ))
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "user_models.db")

        self._db_path = db_path
        self._init_db()
        self._load()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self._db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_models (
                worker_id TEXT PRIMARY KEY,
                beliefs TEXT NOT NULL,
                preferences TEXT NOT NULL DEFAULT '{}',
                interaction_history TEXT NOT NULL DEFAULT '[]',
                updated_at INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _load(self) -> None:
        """Load worker model from SQLite."""
        conn = sqlite3.connect(self._db_path)
        row = conn.execute(
            "SELECT beliefs, preferences, interaction_history FROM user_models WHERE worker_id = ?",
            (self.worker_id,),
        ).fetchone()
        conn.close()

        if row:
            beliefs_dict = json.loads(row[0])
            self.beliefs = {k: WorkerBelief.from_dict(v) for k, v in beliefs_dict.items()}
            self.preferences = json.loads(row[1])
            self.interaction_history = json.loads(row[2])
        else:
            # Initialize with default priors
            for name, (mean, variance) in self.DEFAULT_BELIEFS.items():
                self.beliefs[name] = WorkerBelief(name=name, mean=mean, variance=variance)

    def _save(self) -> None:
        """Persist worker model to SQLite."""
        conn = sqlite3.connect(self._db_path)
        conn.execute(
            """INSERT OR REPLACE INTO user_models
            (worker_id, beliefs, preferences, interaction_history, updated_at)
            VALUES (?, ?, ?, ?, ?)""",
            (
                self.worker_id,
                json.dumps({k: v.to_dict() for k, v in self.beliefs.items()}),
                json.dumps(self.preferences),
                json.dumps(self.interaction_history[-50:]),  # Keep last 50
                int(time.time() * 1000),
            ),
        )
        conn.commit()
        conn.close()

    def update_from_interaction(
        self,
        query: str,
        response: str,
        outcome: str,
        observations: Optional[Dict[str, float]] = None,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update the worker model after an interaction.

        STA 142: Bayesian updating with observed values.
        ECO 201: Learn from production/transaction patterns.

        @param observations Numeric observations to update beliefs with.
            Keys match belief names (e.g., "daily_revenue": 850.0).
        @param preferences Non-numeric preference updates.
        """
        if observations:
            for key, value in observations.items():
                if key in self.beliefs:
                    self.beliefs[key].update(value)
                else:
                    # New belief with low initial confidence
                    self.beliefs[key] = WorkerBelief(
                        name=key, mean=value, variance=100.0, confidence=0.2,
                    )

        if preferences:
            self.preferences.update(preferences)

        # Track interaction for pattern prediction
        self.interaction_history.append({
            "query_summary": query[:100],
            "outcome": outcome,
            "timestamp": time.time(),
        })

        self._save()

    def predict_next_need(self) -> Optional[Dict[str, Any]]:
        """
        Predict what the worker will need next based on patterns.

        Uses simple time-series analysis on interaction history:
        - Restock frequency → next restock time
        - Time-of-day patterns → likely next interaction time
        - Query topic patterns → likely next question type

        ECO 201: Producer theory — predict based on production cycle.
        """
        if len(self.interaction_history) < 3:
            return None

        # Analyze restock frequency
        restock_belief = self.beliefs.get("restock_frequency_days")
        if restock_belief and restock_belief.effective_confidence > 0.3:
            last_interaction = max(h["timestamp"] for h in self.interaction_history)
            days_since = (time.time() - last_interaction) / 86400
            next_restock_days = restock_belief.mean

            if days_since >= next_restock_days * 0.8:
                return {
                    "type": "restock_reminder",
                    "urgency": min(1.0, days_since / next_restock_days),
                    "message": "Worker likely needs to restock soon",
                    "confidence": restock_belief.effective_confidence,
                }

        # Analyze time-of-day patterns
        hours = [time.localtime(h["timestamp"]).tm_hour for h in self.interaction_history[-20:]]
        if hours:
            avg_hour = sum(hours) / len(hours)
            current_hour = time.localtime().tm_hour
            if abs(current_hour - avg_hour) <= 1:
                return {
                    "type": "usual_active_time",
                    "urgency": 0.3,
                    "message": "Worker is usually active around now",
                    "confidence": 0.4,
                }

        return None

    def get_decision_tendency(self, decision_type: str) -> Dict[str, Any]:
        """
        Get the worker's tendency for a type of decision.

        Returns belief mean, variance, and confidence for the decision.
        Useful for: pricing decisions, supplier choices, risk-taking.
        """
        belief = self.beliefs.get(decision_type)
        if belief:
            return {
                "expected": belief.mean,
                "uncertainty": belief.variance,
                "confidence": belief.effective_confidence,
                "observations": belief.update_count,
            }
        return {"expected": None, "uncertainty": 1.0, "confidence": 0.0, "observations": 0}

    def get_profile_summary(self) -> Dict[str, Any]:
        """Get a summary of what we know about this worker."""
        return {
            "worker_id": self.worker_id,
            "total_beliefs": len(self.beliefs),
            "high_confidence_beliefs": {
                k: v.mean for k, v in self.beliefs.items()
                if v.effective_confidence > 0.5
            },
            "preferences": self.preferences,
            "interaction_count": len(self.interaction_history),
            "prediction": self.predict_next_need(),
        }

    def __repr__(self) -> str:
        confident = sum(1 for b in self.beliefs.values() if b.effective_confidence > 0.5)
        return f"WorkerBehavioralModel(worker={self.worker_id[:8]}..., beliefs={len(self.beliefs)}, confident={confident})"


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

    def __init__(
        self,
        agent_id: str,
        event_bus: Optional[AgentEventBus] = None,
        sqlite_store: Optional[SQLiteFTS5Store] = None,
    ):
        self.agent_id = agent_id
        self.event_bus = event_bus or AgentEventBus.get_instance()

        # L2: SQLite FTS5 episodic store (shared across workers)
        self._sqlite_store = sqlite_store or SQLiteFTS5Store()

        # Three tiers (Hermes L1/L2/L3)
        self.working = WorkingMemory(capacity=50)          # L1: Session
        self.episodic = EpisodicMemory(                     # L2: Episodic
            capacity=1000,
            sqlite_store=self._sqlite_store,
        )
        self.long_term = LongTermMemory(capacity=500)       # L3: Patterns

        # L3: Worker behavioral models (one per worker)
        self._worker_models: Dict[str, WorkerBehavioralModel] = {}

        # Consolidation state
        self._last_consolidation = time.time()
        self._consolidation_interval = 3600  # 1 hour

        # Wire up event bus subscriptions
        self._subscribe_to_events()

        logger.info(f"TieredMemoryManager initialized for agent {agent_id} (Hermes L1/L2/L3)")

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
        outcome: str = "neutral",
        lessons: Optional[List[str]] = None,
        business_context: Optional[Dict[str, Any]] = None,
        observations: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Store a conversation turn across all memory tiers.

        L1 (Working): Current session context
        L2 (Episodic): SQLite FTS5 indexed for future retrieval
        L3 (User Model): Bayesian update with observed values
        """
        # L1: Working memory
        self.working.store_interaction(user_input, agent_response, dialect)

        # L2: Episodic memory (SQLite FTS5)
        self.episodic.store_interaction(
            user_input, agent_response, user_id_hash, dialect,
            outcome=outcome, lessons=lessons, business_context=business_context,
        )

        # L3: Update worker behavioral model
        if user_id_hash:
            model = self.get_worker_model(user_id_hash)
            model.update_from_interaction(
                query=user_input,
                response=agent_response,
                outcome=outcome,
                observations=observations,
            )

    # ── Think (Retrieve) ────────────────────────────────────────

    def think(self, query: str, user_id_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve relevant memories from ALL three tiers for a query.

        Hermes pattern: L1 + L2 + L3 retrieval with skill search.

        Returns a context dict with:
        - working_context: Current conversation context (L1)
        - similar_episodes: Past similar interactions via FTS5 (L2)
        - matching_skills: Auto-generated skills from closed learning loop (L2)
        - relevant_patterns: Long-term patterns that apply (L3)
        - failure_warnings: Known failure patterns to avoid (L2)
        - worker_model: What we know about this worker (L3)
        - prediction: What the worker likely needs next (L3)
        """
        # L1: Working memory context
        working_context = self.working.get_context()

        # L2: Episodic recall via FTS5 (sub-10ms)
        similar_episodes = self.episodic.recall_similar(query, limit=5, user_id_hash=user_id_hash)

        # L2: Skill search (closed learning loop)
        matching_skills = []
        if self._sqlite_store:
            matching_skills = self._sqlite_store.search_skills(
                query=query, worker_id=user_id_hash, limit=3,
            )

        # L3: Long-term pattern recall
        relevant_patterns = []
        if user_id_hash:
            relevant_patterns = self.long_term.recall_for_user(user_id_hash, limit=5)

        # L3: Worker behavioral model
        worker_model_summary = None
        prediction = None
        if user_id_hash:
            model = self.get_worker_model(user_id_hash)
            worker_model_summary = model.get_profile_summary()
            prediction = model.predict_next_need()

        # L2: Failure pattern warnings
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
            "matching_skills": matching_skills,
            "relevant_patterns": [
                {"description": p.description, "confidence": p.effective_confidence, "type": p.pattern_type.value}
                for p in relevant_patterns
            ],
            "failure_warnings": failure_warnings,
            "worker_model": worker_model_summary,
            "prediction": prediction,
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
        Run memory consolidation across all three tiers.

        Hermes pattern:
        1. L1: No consolidation needed (session-scoped)
        2. L2: Decay old episodes, FTS5 cleanup
        3. L3: Decay old patterns, distill from episodic

        Returns consolidation stats.
        """
        now = time.time()
        self._last_consolidation = now

        # L2: Decay FTS5 episodes
        fts_removed = 0
        if self._sqlite_store:
            fts_removed = self._sqlite_store.run_decay()

        # L3: Decay long-term patterns
        removed = self.long_term.run_decay()

        # Distill from episodic → long-term
        distilled = self._distill_patterns()

        stats = {
            "patterns_decayed": removed,
            "fts_episodes_decayed": fts_removed,
            "patterns_distilled": distilled,
            "working_memory_size": len(self.working),
            "episodic_memory_size": len(self.episodic),
            "long_term_memory_size": len(self.long_term),
            "worker_models_tracked": len(self._worker_models),
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

    def get_worker_model(self, worker_id: str) -> WorkerBehavioralModel:
        """
        Get or create the L3 behavioral model for a worker.

        Models are cached in memory and persisted to SQLite.
        """
        if worker_id not in self._worker_models:
            self._worker_models[worker_id] = WorkerBehavioralModel(worker_id)
        return self._worker_models[worker_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics across all three tiers."""
        fts_stats = {}
        if self._sqlite_store:
            try:
                conn = self._sqlite_store._get_conn()
                ep_count = conn.execute("SELECT COUNT(*) FROM episodes").fetchone()[0]
                skill_count = conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
                fts_stats = {"episodes": ep_count, "skills": skill_count}
            except Exception:
                pass

        return {
            "agent_id": self.agent_id,
            "l1_working_memory": len(self.working),
            "l2_episodic_memory": len(self.episodic),
            "l2_fts5": fts_stats,
            "l3_long_term_memory": len(self.long_term),
            "l3_worker_models": len(self._worker_models),
            "last_consolidation": self._last_consolidation,
            "event_bus_stats": self.event_bus.get_event_stats(),
        }

    def clear_working(self) -> None:
        """Clear working memory (e.g., new conversation)."""
        self.working.clear()

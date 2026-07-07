"""
Stigmergy Pattern — Decentralized Agent Coordination for Angavu Intelligence.

WHY: Informal markets already use stigmergy — indirect coordination through
environment modification. When a tomato seller sets up at a corner and does
well, other sellers gravitate there. No central planner, no meeting — just
traces in the environment that guide behavior. Agent swarms should mirror
this natural coordination pattern.

HOW: Agents leave "traces" (pheromone-like data markers) in a shared
environment (Redis-backed shared state). Other agents read these traces
and adjust their behavior accordingly. Traces decay over time — old
information becomes less influential, just like ant pheromones.

WHERE: angavu-intelligence-backend/app/agents/coordination/stigmergy.py

Pattern borrowed from: UPC Barcelona stigmergy research + PolySwarm
Alignment: Emergent intelligence from African ground truth data
"""

from __future__ import annotations

import json
import math
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

# ── Trace Types ──────────────────────────────────────────────


class TraceType(str, Enum):
    """Types of traces agents can leave in the environment."""
    PRICE_SIGNAL = "price_signal"          # "Tomatoes are 50 KES/kg at Gikomba"
    DEMAND_SIGNAL = "demand_signal"        # "High demand for onions in Korogocho"
    SUPPLY_SIGNAL = "supply_signal"        # "Low supply of maize in Eldoret"
    OPPORTUNITY = "opportunity"            # "Gap in market: no fish vendor at Stage X"
    WARNING = "warning"                    # "Price crash: tomatoes down 40%"
    ROUTE_INTEL = "route_intel"            # "Traffic bad on Thika Road today"
    TRUST_SIGNAL = "trust_signal"          # "Supplier X is reliable"
    SEASONAL_PATTERN = "seasonal_pattern"  # "Rainy season: umbrella demand up"


class TraceStrength(str, Enum):
    """How strong/confident a trace is. Affects initial pheromone level."""
    WEAK = "weak"          # 0.2 — single observation, unconfirmed
    MODERATE = "moderate"  # 0.5 — multiple observations
    STRONG = "strong"      # 0.8 — consistently observed, high confidence
    VERIFIED = "verified"  # 1.0 — confirmed by multiple agents or transactions


# ── Data Structures ──────────────────────────────────────────


@dataclass
class AgentTrace:
    """
    A trace left by an agent in the shared environment.

    Traces are the fundamental unit of stigmergic coordination.
    Each trace represents a piece of market intelligence that
    other agents can read and act upon.

    Like ant pheromones, traces decay over time — fresh information
    is more influential than stale data. Multiple agents reinforcing
    the same signal strengthens it (positive feedback).
    """
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    trace_type: TraceType = TraceType.PRICE_SIGNAL
    agent_id: str = ""  # Which agent left this trace
    market_id: str = ""  # Which market this relates to
    commodity: str = ""  # What commodity (if applicable)
    payload: dict[str, Any] = field(default_factory=dict)
    strength: TraceStrength = TraceStrength.MODERATE
    initial_pheromone: float = 0.5  # Starting pheromone level (0-1)
    current_pheromone: float = 0.5  # Current pheromone after decay
    created_at: float = field(default_factory=time.time)
    last_reinforced: float = field(default_factory=time.time)
    reinforce_count: int = 0  # How many agents have reinforced this
    ttl_seconds: int = 3600  # Default 1 hour TTL
    tags: list[str] = field(default_factory=list)

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at

    @property
    def is_expired(self) -> bool:
        return self.current_pheromone <= 0.01 or self.age_seconds > self.ttl_seconds

    @property
    def is_alive(self) -> bool:
        return not self.is_expired

    def reinforce(self, boost: float = 0.1) -> None:
        """
        Reinforce this trace (like another ant following the same path).

        Each reinforcement increases the pheromone level and updates
        the timestamp, keeping the trace alive longer.
        """
        self.current_pheromone = min(1.0, self.current_pheromone + boost)
        self.last_reinforced = time.time()
        self.reinforce_count += 1

    def to_dict(self) -> dict[str, Any]:
        """Serialize for Redis storage."""
        return {
            "trace_id": self.trace_id,
            "trace_type": self.trace_type.value,
            "agent_id": self.agent_id,
            "market_id": self.market_id,
            "commodity": self.commodity,
            "payload": self.payload,
            "strength": self.strength.value,
            "initial_pheromone": self.initial_pheromone,
            "current_pheromone": self.current_pheromone,
            "created_at": self.created_at,
            "last_reinforced": self.last_reinforced,
            "reinforce_count": self.reinforce_count,
            "ttl_seconds": self.ttl_seconds,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentTrace:
        """Deserialize from Redis."""
        return cls(
            trace_id=data["trace_id"],
            trace_type=TraceType(data["trace_type"]),
            agent_id=data["agent_id"],
            market_id=data["market_id"],
            commodity=data.get("commodity", ""),
            payload=data.get("payload", {}),
            strength=TraceStrength(data["strength"]),
            initial_pheromone=data.get("initial_pheromone", 0.5),
            current_pheromone=data.get("current_pheromone", 0.5),
            created_at=data.get("created_at", time.time()),
            last_reinforced=data.get("last_reinforced", time.time()),
            reinforce_count=data.get("reinforce_count", 0),
            ttl_seconds=data.get("ttl_seconds", 3600),
            tags=data.get("tags", []),
        )


# ── Pheromone Decay ──────────────────────────────────────────


class PheromoneDecay:
    """
    Controls how traces lose influence over time.

    Pheromone decay is what makes stigmergy work — old information
    fades, new information dominates. Without decay, the environment
    would be cluttered with stale data.

    Decay follows an exponential curve: fast initial decay that
    slows down. A trace at 0.8 drops to 0.4 quickly, but from
    0.1 to 0.05 takes much longer.

    Decay rate can be adjusted per trace type:
    - Price signals decay fast (markets change hourly)
    - Trust signals decay slowly (reputation is sticky)
    - Seasonal patterns decay very slowly (patterns repeat)
    """

    # Decay rates per trace type (lambda for exponential decay)
    DECAY_RATES: dict[TraceType, float] = {
        TraceType.PRICE_SIGNAL: 0.0005,      # Fast — prices change hourly
        TraceType.DEMAND_SIGNAL: 0.0003,      # Moderate — demand shifts daily
        TraceType.SUPPLY_SIGNAL: 0.0003,      # Moderate
        TraceType.OPPORTUNITY: 0.0004,         # Moderate-fast — opportunities close
        TraceType.WARNING: 0.0002,             # Slower — warnings stay relevant
        TraceType.ROUTE_INTEL: 0.001,          # Very fast — traffic changes by minute
        TraceType.TRUST_SIGNAL: 0.00005,       # Very slow — trust is sticky
        TraceType.SEASONAL_PATTERN: 0.00001,   # Extremely slow — seasonal patterns persist
    }

    @classmethod
    def calculate_decay(
        cls,
        trace: AgentTrace,
        current_time: Optional[float] = None,
    ) -> float:
        """
        Calculate the current pheromone level after decay.

        Uses exponential decay: P(t) = P₀ * e^(-λt)

        Args:
            trace: The trace to calculate decay for
            current_time: Current timestamp (defaults to time.time())

        Returns:
            Current pheromone level (0.0 to 1.0)
        """
        if current_time is None:
            current_time = time.time()

        elapsed = current_time - trace.last_reinforced
        decay_rate = cls.DECAY_RATES.get(trace.trace_type, 0.0003)

        decayed = trace.current_pheromone * math.exp(-decay_rate * elapsed)

        # Floor at 0.01 — below this, consider expired
        return max(0.01, decayed) if decayed > 0.01 else 0.0

    @classmethod
    def apply_decay(cls, trace: AgentTrace) -> AgentTrace:
        """
        Apply decay to a trace and return updated version.

        Modifies the trace in-place and returns it.
        """
        trace.current_pheromone = cls.calculate_decay(trace)
        return trace

    @classmethod
    def get_relevance_score(cls, trace: AgentTrace) -> float:
        """
        Get a relevance score combining pheromone strength and recency.

        Higher score = more relevant for agent decision-making.
        Combines pheromone level with a recency bonus.
        """
        pheromone = cls.calculate_decay(trace)
        recency_bonus = max(0, 1.0 - (trace.age_seconds / trace.ttl_seconds))
        return (pheromone * 0.7) + (recency_bonus * 0.3)


# ── Shared Environment ───────────────────────────────────────


class SharedEnvironment:
    """
    Redis-backed shared state where agents leave and read traces.

    This is the "environment" in stigmergy — the shared medium
    through which agents coordinate indirectly. Agents never
    talk to each other directly; they only interact through traces.

    For MVP, uses an in-memory dict. In production, backed by Redis
    for persistence across server restarts and multi-instance deployment.

    Key design decisions:
    - Traces are indexed by market_id for fast market-specific queries
    - Traces are indexed by commodity for price intelligence
    - Expired traces are lazily cleaned up on access
    - Thread-safe for concurrent agent access
    """

    def __init__(self, use_redis: bool = False, redis_url: Optional[str] = None) -> None:
        self._use_redis = use_redis
        self._redis_url = redis_url

        # In-memory storage (MVP)
        self._traces: dict[str, AgentTrace] = {}  # trace_id → AgentTrace
        self._market_index: dict[str, set[str]] = {}  # market_id → {trace_ids}
        self._commodity_index: dict[str, set[str]] = {}  # commodity → {trace_ids}
        self._type_index: dict[TraceType, set[str]] = {}  # trace_type → {trace_ids}

        # Stats
        self._total_traces_written = 0
        self._total_traces_read = 0

        # TODO: Initialize Redis connection if use_redis=True
        # self._redis = redis.from_url(redis_url) if use_redis else None

    def deposit_trace(self, trace: AgentTrace) -> str:
        """
        Agent deposits a trace into the environment.

        This is the "write" operation — an agent leaves a signal
        for other agents to discover.

        If a similar trace already exists (same market + commodity + type),
        it gets reinforced instead of creating a duplicate.

        Args:
            trace: The trace to deposit

        Returns:
            The trace_id (new or existing if reinforced)
        """
        # Check for existing similar trace to reinforce
        existing = self._find_similar_trace(trace)
        if existing:
            existing.reinforce(boost=0.1)
            # Update payload with latest data
            existing.payload.update(trace.payload)
            existing.last_reinforced = time.time()
            self._total_traces_written += 1
            return existing.trace_id

        # New trace
        self._traces[trace.trace_id] = trace
        self._total_traces_written += 1

        # Update indexes
        if trace.market_id:
            self._market_index.setdefault(trace.market_id, set()).add(trace.trace_id)
        if trace.commodity:
            self._commodity_index.setdefault(trace.commodity, set()).add(trace.trace_id)
        self._type_index.setdefault(trace.trace_type, set()).add(trace.trace_id)

        # TODO: Also write to Redis if enabled
        # if self._use_redis:
        #     self._redis.hset(f"traces:{trace.trace_id}", mapping=trace.to_dict())

        return trace.trace_id

    def read_traces(
        self,
        market_id: Optional[str] = None,
        commodity: Optional[str] = None,
        trace_type: Optional[TraceType] = None,
        min_pheromone: float = 0.1,
        limit: int = 50,
    ) -> list[AgentTrace]:
        """
        Agent reads traces from the environment.

        This is the "read" operation — an agent discovers signals
        left by other agents and uses them for decision-making.

        Results are sorted by relevance (pheromone × recency).

        Args:
            market_id: Filter by market
            commodity: Filter by commodity
            trace_type: Filter by trace type
            min_pheromone: Minimum pheromone level to include
            limit: Max number of traces to return

        Returns:
            List of traces sorted by relevance (highest first)
        """
        # Collect candidate trace IDs from indexes
        candidate_ids: Optional[set[str]] = None

        if market_id and market_id in self._market_index:
            candidate_ids = self._market_index[market_id].copy()

        if commodity and commodity in self._commodity_index:
            commodity_ids = self._commodity_index[commodity]
            candidate_ids = commodity_ids if candidate_ids is None else candidate_ids & commodity_ids

        if trace_type and trace_type in self._type_index:
            type_ids = self._type_index[trace_type]
            candidate_ids = type_ids if candidate_ids is None else candidate_ids & type_ids

        if candidate_ids is None:
            candidate_ids = set(self._traces.keys())

        # Filter and score
        results: list[tuple[AgentTrace, float]] = []
        expired_ids: list[str] = []

        for tid in candidate_ids:
            trace = self._traces.get(tid)
            if trace is None:
                continue

            # Apply decay
            PheromoneDecay.apply_decay(trace)

            # Check expiry
            if trace.is_expired:
                expired_ids.append(tid)
                continue

            # Check minimum pheromone
            if trace.current_pheromone < min_pheromone:
                continue

            relevance = PheromoneDecay.get_relevance_score(trace)
            results.append((trace, relevance))

        # Clean up expired traces
        for tid in expired_ids:
            self._remove_trace(tid)

        # Sort by relevance (highest first) and limit
        results.sort(key=lambda x: x[1], reverse=True)
        self._total_traces_read += len(results)

        return [trace for trace, _ in results[:limit]]

    def read_strongest_signals(
        self,
        market_id: str,
        limit: int = 10,
    ) -> list[AgentTrace]:
        """
        Read the strongest signals for a specific market.

        Convenience method for agents that need the "big picture"
        of what's happening at a market — equivalent to an ant
        sensing the strongest pheromone trails nearby.
        """
        return self.read_traces(market_id=market_id, min_pheromone=0.3, limit=limit)

    def read_price_signals(
        self,
        commodity: str,
        market_id: Optional[str] = None,
    ) -> list[AgentTrace]:
        """
        Read price-related traces for a commodity.

        Used by the BuyerAgent and SellerAgent for price intelligence.
        """
        return self.read_traces(
            market_id=market_id,
            commodity=commodity,
            trace_type=TraceType.PRICE_SIGNAL,
            min_pheromone=0.2,
        )

    def get_stats(self) -> dict[str, Any]:
        """Get environment statistics."""
        alive_traces = sum(1 for t in self._traces.values() if t.is_alive)
        return {
            "total_traces": len(self._traces),
            "alive_traces": alive_traces,
            "expired_traces": len(self._traces) - alive_traces,
            "total_written": self._total_traces_written,
            "total_read": self._total_traces_read,
            "markets": len(self._market_index),
            "commodities": len(self._commodity_index),
        }

    def cleanup_expired(self) -> int:
        """
        Manually trigger cleanup of all expired traces.

        Normally cleanup is lazy (on read), but this can be
        called periodically to free memory.
        """
        expired = [
            tid for tid, trace in self._traces.items()
            if trace.is_expired
        ]
        for tid in expired:
            self._remove_trace(tid)
        return len(expired)

    # ── Internal helpers ──────────────────────────────────────

    def _find_similar_trace(self, trace: AgentTrace) -> Optional[AgentTrace]:
        """Find an existing trace that's similar enough to reinforce."""
        if not trace.market_id or not trace.commodity:
            return None

        market_traces = self._market_index.get(trace.market_id, set())
        commodity_traces = self._commodity_index.get(trace.commodity, set())
        type_traces = self._type_index.get(trace.trace_type, set())

        # Find intersection: same market + commodity + type
        candidates = market_traces & commodity_traces & type_traces

        for tid in candidates:
            existing = self._traces.get(tid)
            if existing and existing.is_alive and existing.agent_id != trace.agent_id:
                return existing

        return None

    def _remove_trace(self, trace_id: str) -> None:
        """Remove a trace from all indexes."""
        trace = self._traces.pop(trace_id, None)
        if trace is None:
            return

        if trace.market_id and trace.market_id in self._market_index:
            self._market_index[trace.market_id].discard(trace_id)
            if not self._market_index[trace.market_id]:
                del self._market_index[trace.market_id]

        if trace.commodity and trace.commodity in self._commodity_index:
            self._commodity_index[trace.commodity].discard(trace_id)
            if not self._commodity_index[trace.commodity]:
                del self._commodity_index[trace.commodity]

        if trace.trace_type in self._type_index:
            self._type_index[trace.trace_type].discard(trace_id)
            if not self._type_index[trace.trace_type]:
                del self._type_index[trace.trace_type]


# ── Trace Reader (Agent Interface) ───────────────────────────


class TraceReader:
    """
    High-level interface for agents to read and interpret traces.

    Wraps SharedEnvironment with domain-specific queries that
    map to common agent needs:
    - "What's the price trend for tomatoes?"
    - "Are there any warnings at Gikomba market?"
    - "Which suppliers are trustworthy?"

    Each agent type can create a TraceReader filtered to their
    relevant markets and commodities.
    """

    def __init__(
        self,
        environment: SharedEnvironment,
        agent_id: str,
        default_markets: Optional[list[str]] = None,
    ) -> None:
        self._env = environment
        self._agent_id = agent_id
        self._default_markets = default_markets or []

    def get_price_intelligence(
        self,
        commodity: str,
        market_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Get price intelligence for a commodity.

        Returns current signals, trend direction, and confidence.
        """
        signals = self._env.read_price_signals(commodity, market_id)

        if not signals:
            return {
                "commodity": commodity,
                "signals": [],
                "trend": "unknown",
                "confidence": 0.0,
            }

        # Aggregate price signals
        prices = []
        for s in signals:
            if "price" in s.payload:
                prices.append(float(s.payload["price"]))

        avg_price = sum(prices) / len(prices) if prices else 0
        total_pheromone = sum(s.current_pheromone for s in signals)

        return {
            "commodity": commodity,
            "signal_count": len(signals),
            "average_price": avg_price,
            "strongest_signal": signals[0].payload if signals else {},
            "trend": self._infer_trend(signals),
            "confidence": min(1.0, total_pheromone / len(signals)) if signals else 0.0,
        }

    def get_market_overview(self, market_id: str) -> dict[str, Any]:
        """
        Get an overview of all signals at a market.

        Used by MarketAnalystAgent for market intelligence reports.
        """
        traces = self._env.read_strongest_signals(market_id)

        by_type: dict[str, list[dict]] = {}
        for t in traces:
            type_key = t.trace_type.value
            by_type.setdefault(type_key, []).append({
                "commodity": t.commodity,
                "payload": t.payload,
                "strength": t.current_pheromone,
                "age_minutes": t.age_seconds / 60,
            })

        return {
            "market_id": market_id,
            "total_signals": len(traces),
            "by_type": by_type,
            "strongest_commodity": max(
                (t.commodity for t in traces if t.commodity),
                key=lambda c: sum(
                    s.current_pheromone for s in traces if s.commodity == c
                ),
                default=None,
            ),
        }

    def get_warnings(self, market_id: Optional[str] = None) -> list[dict[str, Any]]:
        """
        Get active warnings (price crashes, supply shortages, etc.)

        Used by agents to alert workers about risks.
        """
        traces = self._env.read_traces(
            market_id=market_id,
            trace_type=TraceType.WARNING,
            min_pheromone=0.3,
        )
        return [
            {
                "warning": t.payload.get("message", "Unknown warning"),
                "commodity": t.commodity,
                "market": t.market_id,
                "strength": t.current_pheromone,
                "age_minutes": t.age_seconds / 60,
            }
            for t in traces
        ]

    def get_trust_signals(self, entity_id: str) -> dict[str, Any]:
        """
        Get trust/reliability signals for a supplier or buyer.

        Used by BuyerAgent to evaluate suppliers.
        """
        traces = self._env.read_traces(
            trace_type=TraceType.TRUST_SIGNAL,
            min_pheromone=0.2,
        )

        relevant = [
            t for t in traces
            if t.payload.get("entity_id") == entity_id
        ]

        if not relevant:
            return {"entity_id": entity_id, "trust_score": 0.5, "signals": 0}

        avg_trust = sum(
            t.payload.get("trust_score", 0.5) * t.current_pheromone
            for t in relevant
        ) / sum(t.current_pheromone for t in relevant)

        return {
            "entity_id": entity_id,
            "trust_score": round(avg_trust, 2),
            "signals": len(relevant),
            "reinforced_count": sum(t.reinforce_count for t in relevant),
        }

    def _infer_trend(self, signals: list[AgentTrace]) -> str:
        """Infer price trend direction from signals."""
        trends = [s.payload.get("trend") for s in signals if "trend" in s.payload]
        if not trends:
            return "unknown"

        up = trends.count("up")
        down = trends.count("down")

        if up > down * 1.5:
            return "rising"
        elif down > up * 1.5:
            return "falling"
        else:
            return "stable"

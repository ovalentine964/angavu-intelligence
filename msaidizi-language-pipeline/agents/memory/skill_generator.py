"""
Skill Generator — Closed Learning Loop (Hermes Pattern)
========================================================

Implements Hermes's closed learning loop for Msaidizi:
  1. Task enters (worker query via WhatsApp/voice)
  2. Skill search — FTS5 query against existing skills
  3. Plan + execute — agent processes with relevant context
  4. Verify — check outcome
  5. Skill generation — if complex task (3+ steps), auto-generate skill
  6. Memory update — outcome logged to L2; L3 user model updated

The closed learning loop is THE differentiating pattern from Hermes.
Workers repeat similar financial tasks daily — the system should get
smarter with each interaction. After two weeks, agencies report 40%
research-task time cuts. For informal workers, this means faster,
more accurate financial guidance over time.

Academic basis:
  - ECO 201 (Producer Theory): Learn from production decisions
  - STA 142 (Statistical Learning): Pattern extraction from outcomes
  - ECO 206 (Microfinance): Financial workflow optimization

Example flow:
  Worker asks about tomato pricing → complex interaction (5+ steps)
  → Skill generated: "Tomato Market Pricing Protocol"
  → Future tomato questions answered faster using learned skill
  → Skill improves as more tomato interactions are observed

@author Angavu Intelligence — Implementation Swarm 14
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ── Configuration ───────────────────────────────────────────────

# Minimum tool calls / steps to trigger skill generation
MIN_COMPLEXITY_FOR_SKILL = 3

# Minimum confidence to store a skill
MIN_SKILL_CONFIDENCE = 0.4

# Maximum skills per worker (prevent bloat)
MAX_SKILLS_PER_WORKER = 100

# Skill template categories for informal economy
SKILL_CATEGORIES = {
    "pricing": {
        "keywords": ["bei", "price", "gharama", "cost", "nunua", "buy", "uza", "sell"],
        "template": "pricing_protocol",
        "academic": "ECO 201 — Producer theory: pricing decisions",
    },
    "inventory": {
        "keywords": ["stock", "hifadhi", "inventory", "bidhaa", "goods", "restock", "agizo"],
        "template": "inventory_management",
        "academic": "ECO 201 — Production function: input management",
    },
    "savings": {
        "keywords": ["akiba", "savings", "weka", "save", "bank", "mpesa", "deni", "debt"],
        "template": "financial_planning",
        "academic": "ECO 206 — Microfinance: savings patterns",
    },
    "market": {
        "keywords": ["soko", "market", "wateja", "customers", "demand", "supply", "msimu", "season"],
        "template": "market_analysis",
        "academic": "ECO 101 — Market dynamics: supply and demand",
    },
    "transport": {
        "keywords": ["usafiri", "transport", "gari", "vehicle", "delivery", "leta", "deliver"],
        "template": "logistics",
        "academic": "ECO 201 — Cost structure: transport optimization",
    },
    "records": {
        "keywords": ["daftari", "records", "register", "sales", "faida", "profit", "hasara", "loss"],
        "template": "record_keeping",
        "academic": "ECO 201 — Financial analysis: profit calculation",
    },
}


# ── Data Classes ────────────────────────────────────────────────

@dataclass
class InteractionTrace:
    """
    A trace of a complex interaction that may generate a skill.

    Captures the full execution path: inputs, steps, outputs, outcome.
    Used to determine if an interaction is complex enough to distill
    into a reusable skill.
    """
    trace_id: str
    worker_id: str
    query: str
    response: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    outcome: str = "neutral"
    tools_used: List[str] = field(default_factory=list)
    lessons: List[str] = field(default_factory=list)
    business_context: Dict[str, Any] = field(default_factory=dict)
    dialect: str = ""
    timestamp: float = field(default_factory=time.time)
    duration_ms: float = 0.0

    @property
    def complexity(self) -> int:
        """Number of distinct steps/tool calls in this interaction."""
        return max(len(self.steps), len(self.tools_used))

    @property
    def is_complex(self) -> bool:
        """Whether this interaction is complex enough to generate a skill."""
        return self.complexity >= MIN_COMPLEXITY_FOR_SKILL


@dataclass
class GeneratedSkill:
    """
    A skill generated from the closed learning loop.

    Skills are reusable patterns extracted from complex successful
    interactions. They're stored in L2 (SQLite FTS5) and searched
    via FTS5 for future similar tasks.
    """
    skill_id: str
    title: str
    body: str  # Markdown skill document
    category: str
    source_traces: List[str] = field(default_factory=list)  # Trace IDs
    confidence: float = 0.5
    usage_count: int = 0
    success_count: int = 0
    business_context: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_used: float = 0.0

    @property
    def success_rate(self) -> float:
        """How often this skill leads to successful outcomes."""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count

    def record_usage(self, success: bool) -> None:
        """Record a usage of this skill."""
        self.usage_count += 1
        if success:
            self.success_count += 1
            self.confidence = min(1.0, self.confidence + 0.05)
        else:
            self.confidence = max(0.1, self.confidence - 0.03)
        self.last_used = time.time()


# ── Skill Generator ─────────────────────────────────────────────

class SkillGenerator:
    """
    Implements the Hermes closed learning loop for Msaidizi.

    After complex successful tasks, auto-generates a skill document
    capturing the procedure, pitfalls, and verification steps.

    The skill is stored in L2 (SQLite FTS5) and searched via FTS5
    for future similar tasks. Over time, skills compound — the more
    a worker uses Msaidizi, the smarter it gets at their specific
    business patterns.

    This is what makes Msaidizi an "AI CFO" rather than a chatbot.

    Academic basis:
      - ECO 201: Producer theory — learn from production decisions
      - STA 142: Statistical learning — extract patterns from outcomes
      - ECO 206: Microfinance — optimize financial workflows
    """

    def __init__(self, episodic_store=None):
        """
        @param episodic_store: SQLiteFTS5Store instance for storing
            generated skills. If None, skills are only held in memory.
        """
        self._episodic_store = episodic_store
        self._pending_traces: Dict[str, InteractionTrace] = {}
        self._generated_skills: Dict[str, GeneratedSkill] = {}
        logger.info("SkillGenerator initialized (closed learning loop)")

    # ── Trace Management ────────────────────────────────────────

    def start_trace(
        self,
        worker_id: str,
        query: str,
        dialect: str = "",
        business_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Start tracing a new interaction.

        Call this when a worker's query begins processing.
        Returns a trace_id for subsequent step recording.
        """
        trace_id = hashlib.sha256(
            f"{worker_id}:{query}:{time.time()}".encode()
        ).hexdigest()[:16]

        self._pending_traces[trace_id] = InteractionTrace(
            trace_id=trace_id,
            worker_id=worker_id,
            query=query,
            response="",
            dialect=dialect,
            business_context=business_context or {},
        )

        return trace_id

    def record_step(
        self,
        trace_id: str,
        step_type: str,
        description: str,
        tool_used: str = "",
        output: str = "",
    ) -> None:
        """
        Record a step in an ongoing interaction.

        @param step_type: "search", "calculate", "lookup", "generate", etc.
        @param description: What this step does
        @param tool_used: Tool/function name if applicable
        @param output: Step output summary
        """
        trace = self._pending_traces.get(trace_id)
        if not trace:
            return

        trace.steps.append({
            "type": step_type,
            "description": description,
            "tool": tool_used,
            "output": output[:200],  # Truncate for storage
            "timestamp": time.time(),
        })

        if tool_used and tool_used not in trace.tools_used:
            trace.tools_used.append(tool_used)

    def end_trace(
        self,
        trace_id: str,
        response: str,
        outcome: str = "neutral",
        lessons: Optional[List[str]] = None,
        duration_ms: float = 0.0,
    ) -> Optional[GeneratedSkill]:
        """
        End a trace and evaluate if a skill should be generated.

        Returns a GeneratedSkill if the interaction was complex enough
        and successful enough to warrant a reusable skill.

        This is the core of the closed learning loop:
          trace → evaluate → generate → store → reuse
        """
        trace = self._pending_traces.pop(trace_id, None)
        if not trace:
            return None

        trace.response = response
        trace.outcome = outcome
        trace.lessons = lessons or []
        trace.duration_ms = duration_ms

        # Decide: should we generate a skill from this trace?
        if not trace.is_complex:
            logger.debug(
                f"Trace {trace_id} not complex enough ({trace.complexity} < {MIN_COMPLEXITY_FOR_SKILL})"
            )
            return None

        if outcome not in ("success", "neutral"):
            logger.debug(f"Trace {trace_id} outcome '{outcome}' — not generating skill")
            return None

        # Generate the skill
        skill = self._generate_skill(trace)
        if skill and skill.confidence >= MIN_SKILL_CONFIDENCE:
            self._store_skill(skill)
            logger.info(
                f"Generated skill '{skill.title}' from trace {trace_id} "
                f"(confidence={skill.confidence:.2f}, complexity={trace.complexity})"
            )
            return skill

        return None

    # ── Skill Search (for the retrieval phase) ──────────────────

    def search_skills(
        self,
        query: str,
        worker_id: Optional[str] = None,
        limit: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Search for existing skills that match a query.

        This is step 2 of the closed learning loop: before executing
        a task, search for existing skills that might help.

        Uses FTS5 when available, falls back to in-memory search.
        """
        # Try SQLite FTS5 first (sub-10ms)
        if self._episodic_store:
            results = self._episodic_store.search_skills(
                query=query, worker_id=worker_id, limit=limit,
            )
            if results:
                return results

        # Fallback: in-memory keyword search
        query_words = set(query.lower().split())
        scored = []

        for skill in self._generated_skills.values():
            skill_text = f"{skill.title} {skill.body}".lower()
            skill_words = set(skill_text.split())
            overlap = len(query_words & skill_words)
            if overlap > 0:
                similarity = overlap / max(len(query_words), 1)
                score = similarity * skill.confidence
                scored.append((score, skill))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            {
                "skill_id": s.skill_id,
                "title": s.title,
                "body": s.body,
                "confidence": s.confidence,
                "category": s.category,
                "usage_count": s.usage_count,
                "success_rate": s.success_rate,
            }
            for _, s in scored[:limit]
        ]

    def record_skill_usage(self, skill_id: str, success: bool) -> None:
        """
        Record that a skill was used and whether it succeeded.

        Updates the skill's confidence via Bayesian-style adjustment.
        """
        skill = self._generated_skills.get(skill_id)
        if skill:
            skill.record_usage(success)
            # Update in SQLite if available
            if self._episodic_store:
                self._episodic_store.store_skill(
                    skill_id=skill.skill_id,
                    worker_id="",  # Already stored
                    title=skill.title,
                    body=skill.body,
                    confidence=skill.confidence,
                    business_context=skill.business_context,
                )

    # ── Skill Generation ────────────────────────────────────────

    def _generate_skill(self, trace: InteractionTrace) -> Optional[GeneratedSkill]:
        """
        Generate a skill document from a complex interaction trace.

        Creates a Markdown skill document that captures:
        - What the task was
        - What steps were taken
        - What worked and what didn't
        - How to verify success
        - Pitfalls to avoid

        ECO 201: Skill captures the production process for reuse.
        """
        # Categorize the skill
        category = self._categorize_interaction(trace)

        # Build the skill title
        title = self._generate_title(trace, category)

        # Build the skill body (Markdown document)
        body = self._generate_body(trace, category)

        # Calculate confidence based on trace quality
        confidence = self._calculate_confidence(trace)

        skill_id = f"skill_{trace.trace_id}_{int(time.time())}"

        return GeneratedSkill(
            skill_id=skill_id,
            title=title,
            body=body,
            category=category,
            source_traces=[trace.trace_id],
            confidence=confidence,
            business_context=trace.business_context,
        )

    def _categorize_interaction(self, trace: InteractionTrace) -> str:
        """Categorize an interaction into a skill category."""
        text = f"{trace.query} {trace.response}".lower()

        best_category = "general"
        best_score = 0

        for cat_name, cat_info in SKILL_CATEGORIES.items():
            score = sum(1 for kw in cat_info["keywords"] if kw in text)
            if score > best_score:
                best_score = score
                best_category = cat_name

        return best_category

    def _generate_title(self, trace: InteractionTrace, category: str) -> str:
        """Generate a human-readable skill title."""
        # Extract key nouns from the query
        query_words = trace.query.split()[:6]
        key_phrase = " ".join(query_words)

        category_display = category.replace("_", " ").title()
        return f"{category_display}: {key_phrase}"

    def _generate_body(self, trace: InteractionTrace, category: str) -> str:
        """
        Generate the Markdown skill document.

        Follows the Hermes skill format: procedure, pitfalls,
        verification steps.
        """
        cat_info = SKILL_CATEGORIES.get(category, {})
        academic_basis = cat_info.get("academic", "General knowledge")

        # Build procedure from trace steps
        procedure_lines = []
        for i, step in enumerate(trace.steps, 1):
            tool_info = f" (using {step['tool']})" if step.get("tool") else ""
            procedure_lines.append(f"{i}. {step['description']}{tool_info}")

        procedure = "\n".join(procedure_lines) if procedure_lines else "1. Process the request"

        # Extract lessons as pitfalls
        pitfalls = "\n".join(
            f"- {lesson}" for lesson in trace.lessons
        ) if trace.lessons else "- No specific pitfalls identified yet"

        # Business context
        context_lines = []
        if trace.business_context:
            for key, value in trace.business_context.items():
                context_lines.append(f"- {key}: {value}")
        context_section = "\n".join(context_lines) if context_lines else "- No specific context"

        body = f"""# {self._generate_title(trace, category)}

**Category:** {category.replace('_', ' ').title()}
**Academic Basis:** {academic_basis}
**Generated:** {time.strftime('%Y-%m-%d %H:%M', time.localtime(trace.timestamp))}
**Complexity:** {trace.complexity} steps
**Confidence:** {trace.outcome}

## When This Applies

Worker query pattern: "{trace.query[:100]}"

Business context:
{context_section}

## Procedure

{procedure}

## Pitfalls to Avoid

{pitfalls}

## Verification

- Confirm the worker's need was addressed
- Check that the response was in the correct dialect ({trace.dialect or 'default'})
- Verify any calculations or prices mentioned

## Usage Stats

- Times used: 0
- Success rate: N/A (newly generated)
- Source trace: {trace.trace_id}
"""
        return body

    def _calculate_confidence(self, trace: InteractionTrace) -> float:
        """
        Calculate initial confidence for a generated skill.

        Based on:
        - Outcome quality (success > neutral > failure)
        - Complexity (more steps = more learning)
        - Duration (reasonable duration = better quality)
        - Lessons learned (more lessons = more insight)
        """
        score = 0.3  # Base

        # Outcome bonus
        if trace.outcome == "success":
            score += 0.3
        elif trace.outcome == "neutral":
            score += 0.1

        # Complexity bonus (diminishing returns)
        complexity_bonus = min(0.2, trace.complexity * 0.05)
        score += complexity_bonus

        # Lesson bonus
        lesson_bonus = min(0.15, len(trace.lessons) * 0.05)
        score += lesson_bonus

        # Duration sanity check (too fast or too slow = lower confidence)
        if trace.duration_ms > 0:
            if 1000 < trace.duration_ms < 30000:  # 1-30 seconds is reasonable
                score += 0.05

        return min(1.0, max(0.1, score))

    def _store_skill(self, skill: GeneratedSkill) -> None:
        """Store a generated skill in both memory and SQLite."""
        self._generated_skills[skill.skill_id] = skill

        # Persist to SQLite FTS5
        if self._episodic_store:
            self._episodic_store.store_skill(
                skill_id=skill.skill_id,
                worker_id=skill.business_context.get("worker_id", ""),
                title=skill.title,
                body=skill.body,
                source_episode_id=skill.source_traces[0] if skill.source_traces else None,
                confidence=skill.confidence,
                business_context=skill.business_context,
            )

    # ── Stats ────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get skill generator statistics."""
        skills = list(self._generated_skills.values())
        return {
            "total_skills": len(skills),
            "categories": {
                cat: sum(1 for s in skills if s.category == cat)
                for cat in set(s.category for s in skills)
            } if skills else {},
            "avg_confidence": (
                sum(s.confidence for s in skills) / len(skills) if skills else 0.0
            ),
            "avg_usage": (
                sum(s.usage_count for s in skills) / len(skills) if skills else 0.0
            ),
            "pending_traces": len(self._pending_traces),
        }

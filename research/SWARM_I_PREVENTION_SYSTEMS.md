# 🛡️ Swarm I: Prevention Systems Design — Summary

> **Team:** Swarm I — Prevention Systems Design
> **Date:** 2026-07-07
> **Status:** ✅ Complete
> **Purpose:** Prevent the 10 repeated mistakes from the Angavu Intelligence session

---

## Problem Statement

Throughout the Angavu Intelligence development session, the same 10 mistakes repeated across dozens of swarms and teams. These weren't random — they're systemic failures that any AI agent orchestration will encounter. The solutions must be reusable, practical, and immediately deployable.

---

## The 10 Mistakes and Their Prevention Systems

### 1. Sub-Agent File I/O Not Persisting
**Prevention:** Swarm Coordinator Skill (`skills/SWARM_COORDINATOR.md`)
- Explicit file ownership tracking
- Post-completion verification (check files actually exist on disk)
- Retry-on-failure pattern

### 2. Research Without Implementation Directions
**Prevention:** Review-Fix Pipeline (`skills/REVIEW_FIX_PIPELINE.md`)
- Stage 1 (Research) REQUIRES an "Implementation Directions" section
- WHAT, HOW, WHERE, WHY must all be specified
- Research without directions is rejected and sent back

### 3. Surface-Level Validation
**Prevention:** Verification Script (`scripts/verify_code.py`)
- Actually reads file contents (not just existence checks)
- Checks for paid API references via regex
- Validates Python syntax via `compile()`
- Checks academic framework completeness
- Verifies test files exist for source files
- Reports file content quality (non-trivial line count)

### 4. Paid APIs in Fallback Chain
**Prevention:** Cost Guard (`scripts/cost_guard.py`)
- Pre-commit hook that blocks paid API references
- Scans for OpenAI, Anthropic, Google, DeepSeek, Cohere, Mistral, Perplexity
- Checks dependency files (requirements.txt, package.json)
- Checks for hardcoded API keys
- Installable as git pre-commit hook

### 5. Academic Framework Incomplete
**Prevention:** Academic Completeness Checker (`scripts/academic_completeness.py`)
- Verifies ALL 72 degree units (ECO, STA, MAT, BCB, BIT)
- Flexible pattern matching (ECO101, "ECO 101", eco101, etc.)
- Reports missing units by department
- Supports text, JSON, and markdown output

### 6. Duplicate Work
**Prevention:** Swarm Coordinator Skill (`skills/SWARM_COORDINATOR.md`)
- Component ownership registry
- File-level locking (no two swarms on same file)
- Task registry with status tracking
- Pre-flight checks before task assignment

### 7. No Verification Loop
**Prevention:** Review-Fix Pipeline (`skills/REVIEW_FIX_PIPELINE.md`)
- Mandatory pipeline: Research → Review → Fix → Verify → Commit
- Each stage has specific gates that must pass
- Verification runs actual scripts, not manual checks
- No stage can be skipped

### 8. Swarm Timeouts
**Prevention:** Task Decomposition Skill (`skills/TASK_DECOMPOSITION.md`)
- Max 3-5 files per swarm
- Max 10-minute scope per swarm
- Decomposition patterns (horizontal, vertical, core+extensions)
- Clear checklist before assigning tasks

### 9. Missing Context Between Swarms
**Prevention:** Swarm Coordinator Skill (`skills/SWARM_COORDINATOR.md`)
- Context injection before each swarm starts
- Prior work summary included in task context
- Component ownership visible to all swarms
- Dependency outputs shared with dependent tasks

### 10. No Clear Ownership
**Prevention:** Swarm Coordinator Skill (`skills/SWARM_COORDINATOR.md`)
- Component ownership registry in `swarm_registry.json`
- File-level ownership with claim/release mechanism
- Task ID convention (SWARM-X, IMPL-N, FIX-N, REVIEW-N)
- Status tracking: Pending → In Progress → Verified → Done

---

## Deliverables Created

| # | File | Type | Purpose |
|---|------|------|---------|
| 1 | `skills/SWARM_TASK_TEMPLATE.md` | Skill | Standardized task format for every swarm |
| 2 | `scripts/verify_code.py` | Script | Real code verification (reads content, not just existence) |
| 3 | `scripts/cost_guard.py` | Script | Pre-commit hook blocking paid APIs |
| 4 | `scripts/academic_completeness.py` | Script | Verify all 72 degree units are mapped |
| 5 | `skills/SWARM_COORDINATOR.md` | Skill | Prevent duplicate work, track ownership |
| 6 | `skills/TASK_DECOMPOSITION.md` | Skill | Break large tasks into swarm-sized chunks |
| 7 | `skills/REVIEW_FIX_PIPELINE.md` | Skill | Standardized quality pipeline |

---

## Script Verification Results

All scripts tested and confirmed working:

```
✅ verify_code.py — Syntax check: All Python files valid
✅ cost_guard.py — Found violations in research docs (expected — they reference paid APIs for comparison)
✅ academic_completeness.py — 100% coverage (72/72 units mapped)
```

### Cost Guard Findings (Existing Codebase)
The cost guard correctly identified paid API references in research documents:
- `research/FINAL_REVIEW.md` — mentions DEEPSEEK_API_KEY in settings review
- `research/IMPL_1_VOICE_PIPELINE.md` — comparison table references GPT-4o, Claude
- `research/OPEN_SOURCE_MODELS_COMPARISON.md` — mentions DeepSeek training cost

These are **informational references** in research docs, not actual code usage. The cost guard should be tuned to exclude `.md` files in the `research/` directory for production use, or add a whitelist for documentation.

---

## How to Use These Systems

### For Angavu Intelligence Development

1. **Before any swarm task:** Use `SWARM_TASK_TEMPLATE.md` to define the task
2. **Before assigning:** Run `TASK_DECOMPOSITION.md` checklist (≤5 files, ≤10 min)
3. **During work:** Coordinator tracks ownership via `SWARM_COORDINATOR.md`
4. **After completion:** Run `verify_code.py` + `cost_guard.py`
5. **For any code change:** Follow `REVIEW_FIX_PIPELINE.md`

### For Any Developer Building with AI Agents

These systems are **framework-agnostic**. They work with:
- OpenClaw sub-agents
- LangChain/LangGraph
- CrewAI
- AutoGen
- Custom agent frameworks

The core principles are universal:
1. **Standardize task format** — so agents know what to do
2. **Verify actual content** — not just file existence
3. **Guard costs** — prevent paid API creep
4. **Track ownership** — prevent duplicate work
5. **Decompose tasks** — prevent timeouts
6. **Enforce pipeline** — prevent skipped quality steps

---

## Integration with OpenClaw

### Sub-Agent Pattern
```
Main Session (Coordinator)
├── Creates task in SWARM_TASK_TEMPLATE format
├── Spawns sub-agent with task + context
├── Uses sessions_yield to wait
├── Collects results
├── Runs verification scripts
└── Updates task registry
```

### File Persistence Pattern
```
Sub-agent writes to: /home/work/.openclaw/workspace/<project>/
Main session verifies: test -s <filepath>
On failure: Re-spawn with explicit write path
```

---

## Recommendations for Valentine

1. **Install cost_guard as pre-commit hook:** `python3 scripts/cost_guard.py --install-hook`
2. **Add verification to CI:** Run `verify_code.py` in CI pipeline
3. **Tune cost_guard:** Add whitelist for research docs that reference paid APIs for comparison
4. **Update academic_completeness.py:** If degree units change, update the unit list
5. **Use SWARM_TASK_TEMPLATE for ALL tasks:** Even internal/personal work

---

## Files Produced

```
skills/SWARM_TASK_TEMPLATE.md          — 4.3 KB — Standardized task template
scripts/verify_code.py                 — 19 KB  — Real verification script
scripts/cost_guard.py                  — 9.3 KB — Pre-commit cost checker
scripts/academic_completeness.py       — 10 KB  — Degree unit checker
skills/SWARM_COORDINATOR.md            — 10 KB  — Coordinator skill
skills/TASK_DECOMPOSITION.md           — 7.5 KB — Decomposition skill
skills/REVIEW_FIX_PIPELINE.md          — 7.8 KB — Pipeline skill
research/SWARM_I_PREVENTION_SYSTEMS.md — This file
```

**Total:** ~68 KB of prevention systems.

---

## The Meta-Lesson

The biggest mistake wasn't any individual error — it was **not having systems to prevent errors**. Every fix team was reactive. These prevention systems make quality proactive.

Build the guardrails before you drive. 🛡️

---

*Swarm I — Prevention Systems Design*
*Angavu Intelligence*
*2026-07-07*

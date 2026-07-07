# 🛡️ Swarm Task Template — Prevention System #1

> **Purpose:** Every swarm/sub-agent task MUST use this template. No exceptions.
> **Prevents:** Vague tasks, missing context, no verification, duplicate work, cost overruns.

---

## Required Template

```markdown
# SWARM TASK: [Short Name]

## META
- **Task ID:** [UNIQUE-ID, e.g., IMPL-18, FIX-6, SWARM-I]
- **Owner:** [Agent/swarm name]
- **Dependencies:** [List task IDs that must complete first, or "None"]
- **Timeout:** [Estimated time, max 10 min per swarm]
- **Status:** ⬜ Pending → 🔄 In Progress → ✅ Verified → 🏁 Done

---

## WHY (Business Reason)
[1-2 sentences. Why does this matter? What breaks without it?]

## WHAT (Specific Deliverables)
[Exact files to create/modify. Be specific — no "improve the codebase".]

Example:
- [ ] Create `src/services/model_router.py` — free-only model routing
- [ ] Update `config/providers.json` — remove paid API entries
- [ ] Add `tests/test_model_router.py` — unit tests for routing logic

## HOW (Implementation Steps)
[Numbered steps. Each step should take < 2 minutes.]

1. Read existing `src/services/model_router.py` to understand current state
2. Remove all references to OpenAI, Anthropic, Google APIs
3. Add free providers: HuggingFace, Ollama, local models
4. Write unit tests
5. Run `python -m pytest tests/test_model_router.py`
6. Verify no paid API references: `grep -r "openai\|anthropic\|google" src/`

## WHERE (Exact File Paths)
```
# Files to CREATE:
src/services/model_router.py
tests/test_model_router.py

# Files to MODIFY:
config/providers.json

# Files to READ (context only):
docs/architecture.md
```

## VERIFY (Completion Criteria)
[How to confirm it's ACTUALLY done. Not "looks good" — specific checks.]

```bash
# 1. Files exist AND have content
test -s src/services/model_router.py || exit 1
test -s tests/test_model_router.py || exit 1

# 2. No paid API references
! grep -ri "openai\|anthropic\|claude\|gpt-4\|gemini" src/ || exit 1

# 3. Python syntax valid
python -m py_compile src/services/model_router.py || exit 1

# 4. Tests pass
python -m pytest tests/test_model_router.py -v || exit 1
```

## COST (Budget Constraint)
- [ ] Zero paid APIs (OpenAI, Anthropic, Google, DeepSeek paid tiers)
- [ ] Zero paid cloud services (AWS, GCP, Azure unless explicitly approved)
- [ ] Zero paid dependencies (check `requirements.txt` and `package.json`)
- **Budget:** $0 unless explicitly approved by Valentine Owuor

## CONTEXT (What Other Swarms Did)
[Paste relevant context from prior swarms. Don't make this swarm guess.]

Example:
- Swarm H found trending tools at `research/SWARM_H_TRENDING_TOOLS.md`
- Impl 17 implemented some at `src/services/trending/`
- This task extends that work — don't duplicate.

## OUTPUT FORMAT
When complete, report:
```
✅ TASK [ID] COMPLETE
Files created/modified: [list]
Verification results: [pass/fail for each check]
Time taken: [minutes]
Issues encountered: [any blockers]
```
```

---

## Template Rules

### 1. No Task Without This Template
If a swarm doesn't have a task in this format, it should CREATE one before starting work.

### 2. Task ID Convention
- `SWARM-X` — Research swarms
- `IMPL-N` — Implementation tasks
- `FIX-N` — Bug fix tasks
- `REVIEW-N` — Review tasks
- `SCALABILITY-N` — Scalability tasks

### 3. Timeout Enforcement
- Max 10 minutes per swarm
- If task is larger, decompose using `TASK_DECOMPOSITION.md`
- Never give a swarm more than it can finish

### 4. Dependency Tracking
- Each task lists its dependencies
- Coordinator verifies dependencies are ✅ Done before starting
- No circular dependencies

### 5. Context Injection
- The coordinator MUST inject relevant context from prior swarms
- Include file paths, prior decisions, current state
- Don't make swarms search for context

---

## Anti-Patterns (What NOT to Do)

| ❌ Anti-Pattern | ✅ Correct |
|---|---|
| "Improve the codebase" | "Add PQC stubs to `src/crypto/kyber.py`" |
| "Review everything" | "Check `src/services/` for paid API refs" |
| "Fix the bugs" | "Fix timeout in `src/swarm/coordinator.py` line 42" |
| "Make it better" | "Add error handling to `model_router.py:fetch()`" |
| No verification | 3+ specific bash checks |
| No cost check | Explicit `$0` budget + grep check |
| No context | Paste prior swarm findings |

---

*This template is a living document. Update it as we learn what works.*

# 🛡️ Review-Fix Pipeline — Prevention System #8

> **Purpose:** Standardized pipeline that ensures quality at every stage.
> **Prevents:** Surface-level reviews, unverified implementations, broken code shipping.

---

## The Pipeline

```
Research → Review → Fix → Verify → Commit
    ↑         ↓        ↓        ↓         ↓
  context   issues   fixes    tests    shipped
```

**Every stage must complete before the next begins. No shortcuts.**

---

## Stage 1: Research

### Goal
Understand what exists, what's needed, and what approach to take.

### Input
- Problem statement
- Existing codebase

### Output (REQUIRED)
A research document containing:

```markdown
# Research: [Topic]

## Current State
- What exists now
- What files are involved
- What's working, what's broken

## Findings
- [Specific finding 1 with file:line reference]
- [Specific finding 2 with file:line reference]

## Recommended Approach
- What to implement/change
- What files to create/modify
- What the code should do (pseudocode acceptable)

## Implementation Directions (CRITICAL)
- WHAT: [exact deliverables]
- HOW: [step-by-step approach]
- WHERE: [exact file paths]
- WHY: [business/technical reason]

## Cost Implications
- [ ] Must be $0 (zero paid APIs)
- [ ] Free alternatives: [list]
```

### Gate
Research is NOT complete without "Implementation Directions" section. If a research swarm produces findings without directions, send it back.

---

## Stage 2: Review

### Goal
Identify specific issues in the current codebase.

### Input
- Research findings from Stage 1
- Current codebase

### Output (REQUIRED)
A review document containing:

```markdown
# Review: [Topic]

## Issues Found

### Issue 1: [Short description]
- **Severity:** Critical / High / Medium / Low
- **File:** path/to/file.py:42
- **Problem:** [What's wrong]
- **Impact:** [What breaks]
- **Fix:** [How to fix it]

### Issue 2: [Short description]
...

## Review Checklist (ALL must be checked)

### Code Quality
- [ ] No syntax errors (verified with `python -m py_compile`)
- [ ] No bare `except` clauses
- [ ] No hardcoded credentials
- [ ] Consistent naming conventions

### Cost Compliance
- [ ] No paid API references (verified with cost_guard.py)
- [ ] No paid dependencies
- [ ] No paid cloud services

### Academic Framework
- [ ] All relevant degree units mapped (verified with academic_completeness.py)
- [ ] Non-parametric methods included
- [ ] Multivariate analysis included
- [ ] Econometrics chain complete

### Security
- [ ] No SQL injection vectors
- [ ] No XSS vulnerabilities
- [ ] PQC stubs present
- [ ] No hardcoded secrets

### Completeness
- [ ] All files have content (not empty stubs)
- [ ] All functions implemented (not just `pass`)
- [ ] Tests exist for new code
- [ ] Documentation updated
```

### Gate
Review is NOT complete without running the actual verification scripts. A review that says "looks good" without running `verify_code.py` is INVALID.

---

## Stage 3: Fix

### Goal
Address all issues found in the review.

### Input
- Review document from Stage 2
- Current codebase

### Output (REQUIRED)
- Modified files with fixes applied
- Fix report documenting what was changed

```markdown
# Fix Report: [Topic]

## Fixes Applied

### Fix 1: [Short description]
- **Issue:** [Reference to review issue]
- **File:** path/to/file.py
- **Change:** [What was changed and why]
- **Lines affected:** 42-58

### Fix 2: [Short description]
...

## Files Modified
- path/to/file1.py: [summary of changes]
- path/to/file2.py: [summary of changes]

## Verification
- [ ] Syntax check passed
- [ ] Cost check passed
- [ ] Tests passed
```

### Gate
Fixes are NOT complete without running verification. Every fix must be verified.

---

## Stage 4: Verify

### Goal
Confirm that fixes actually work and nothing is broken.

### Input
- Fixed code from Stage 3

### Verification Steps (ALL REQUIRED)

```bash
# Step 1: Syntax Check
python scripts/verify_code.py --checks syntax

# Step 2: Cost Check
python scripts/cost_guard.py --root .

# Step 3: Content Verification
python scripts/verify_code.py --checks content

# Step 4: Academic Completeness (if applicable)
python scripts/academic_completeness.py --root .

# Step 5: Test Execution
python scripts/verify_code.py --checks tests

# Step 6: PQC Check
python scripts/verify_code.py --checks pqc
```

### Output (REQUIRED)
Verification report:

```markdown
# Verification Report: [Topic]

## Results

| Check | Status | Details |
|-------|--------|---------|
| Syntax | ✅ Pass | All Python files valid |
| Cost | ✅ Pass | No paid API references |
| Content | ✅ Pass | All files have content |
| Academic | ⚠️ 95% | 2 units missing: ECO307, STA308 |
| Tests | ✅ Pass | 12 tests, 0 failures |
| PQC | ⚠️ Warning | PQC stubs present but flags missing |

## Summary
- **Critical issues:** 0
- **Warnings:** 2
- **Can proceed:** Yes (warnings are non-blocking)
```

### Gate
Verification is NOT complete if ANY critical check fails. Warnings may be acceptable depending on context.

---

## Stage 5: Commit

### Goal
Ship the verified code.

### Input
- Verified code from Stage 4
- Verification report

### Steps

```bash
# 1. Final cost check (pre-commit hook runs automatically)
python scripts/cost_guard.py --staged

# 2. Stage changes
git add <modified files>

# 3. Commit with descriptive message
git commit -m "[Task-ID] Description of changes"

# 4. Update task registry
python coordinator.py complete --id <task-id>
```

### Output
- Git commit with task ID reference
- Updated task registry
- Completion notification to coordinator

---

## Pipeline Enforcement

### The Pipeline is MANDATORY

No code reaches `main` without going through all 5 stages.

### Skipping Stages is FORBIDDEN

| Skip Attempted | Response |
|---|---|
| "I'll just commit it" | Blocked by cost_guard pre-commit hook |
| "Review is just a formality" | Review must run verify_code.py |
| "Fixes are obvious" | Every fix must be documented and verified |
| "Tests can wait" | Tests are part of verification gate |

### Escalation

If a stage fails:
1. **Research incomplete** → Send back with specific questions
2. **Review finds critical issues** → Must fix before proceeding
3. **Fix doesn't work** → Return to Fix stage with error details
4. **Verification fails** → Return to Fix stage with verification output
5. **Repeated failures** → Escalate to human (Valentine)

---

## Quick Reference

### For Coordinators
```
1. Start with research (or provide context from prior research)
2. Review must use actual scripts, not manual checks
3. Fix must document every change
4. Verify must run ALL checks, not just syntax
5. Commit only after verification passes
```

### For Swarms
```
1. You're in ONE stage — do that stage well
2. Your output is the next stage's input — be thorough
3. Don't skip verification — it's not optional
4. Document everything — future swarms need your context
5. If you can't finish, report what you DID do
```

---

## Pipeline Visualization

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ RESEARCH │────▶│  REVIEW  │────▶│   FIX   │────▶│ VERIFY  │────▶│ COMMIT  │
│          │     │          │     │          │     │          │     │          │
│ • Find   │     │ • Issues │     │ • Fix   │     │ • Tests  │     │ • Ship  │
│ • Plan   │     │ • Checks │     │ • Doc   │     │ • Cost   │     │ • Track │
│ • Direct │     │ • Scripts│     │ • Code  │     │ • Syntax │     │ • Done  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
     │                │                │                │
     └────────────────┴────────────────┴────────────────┘
                    GATE: Each must pass before next begins
```

---

*This pipeline prevents the most common failure mode: reported-as-done but not actually done.*

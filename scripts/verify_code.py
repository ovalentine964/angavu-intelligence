#!/usr/bin/env python3
"""
🛡️ Verification Script — Prevention System #2

ACTUALLY verifies code quality, not just file existence.
Reads file contents, checks logic, validates completeness.

Usage:
    python verify_code.py [--project-root /path/to/project] [--checks all|cost|academic|pqc|syntax|tests]
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ─── Configuration ───────────────────────────────────────────────

PAID_API_PATTERNS = [
    # OpenAI
    r'openai[\._]',
    r'OpenAI',
    r'gpt-3\.5',
    r'gpt-4',
    r'gpt-4o',
    r'o1-preview',
    r'o1-mini',
    r'chat\.completions',
    # Anthropic
    r'anthropic',
    r'Anthropic',
    r'claude-3',
    r'claude-2',
    r'messages\.create',
    # Google (paid)
    r'gemini-pro',
    r'gemini-ultra',
    r'generativeai',
    r'google\.generativeai',
    # DeepSeek (paid tiers)
    r'deepseek\.com/v1',
    r'api\.deepseek',
    # Cohere
    r'cohere\.',
    r'COHERE_API_KEY',
    # Mistral (paid)
    r'mistral\.ai/v1',
    r'api\.mistral',
    # Perplexity
    r'perplexity\.ai',
    # Generic paid API indicators
    r'API_KEY\s*=\s*["\']sk-',
    r'api_key.*=.*["\']sk-',
]

PAID_DEPENDENCY_PATTERNS = [
    r'openai',
    r'anthropic',
    r'google-generativeai',
    r'cohere',
    r'mistralai',
    r'perplexity',
]

PAID_SERVICE_PATTERNS = [
    r'aws\.amazon\.com',
    r'console\.cloud\.google',
    r'portal\.azure\.com',
    r'lambda\.amazonaws\.com',
    r'cloudfunctions\.googleapis',
    r'azurewebsites\.net',
]

# Academic framework: Economics & Statistics degree units
ACADEMIC_UNITS = {
    # Economics (ECO)
    'ECO': {
        '100': 'Introduction to Economics',
        '101': 'Microeconomics I',
        '102': 'Macroeconomics I',
        '200': 'Intermediate Microeconomics',
        '201': 'Intermediate Macroeconomics',
        '202': 'Mathematical Economics',
        '203': 'Econometrics I',
        '204': 'Development Economics',
        '205': 'International Economics',
        '206': 'Public Finance',
        '207': 'Money and Banking',
        '208': 'Agricultural Economics',
        '300': 'Advanced Microeconomics',
        '301': 'Advanced Macroeconomics',
        '302': 'Econometrics II',
        '303': 'Economics of Planning',
        '304': 'Labor Economics',
        '305': 'Environmental Economics',
        '306': 'Health Economics',
        '307': 'Economics of Education',
        '308': 'Industrial Organization',
        '309': 'Transport Economics',
        '400': 'Advanced Econometrics',
        '401': 'Economic Policy Analysis',
        '402': 'Game Theory',
        '403': 'Behavioral Economics',
        '404': 'Financial Economics',
        '424': 'Research Project',
    },
    # Statistics (STA)
    'STA': {
        '142': 'Introduction to Probability',
        '143': 'Introduction to Statistics',
        '200': 'Probability I',
        '201': 'Statistical Inference I',
        '202': 'Regression Analysis',
        '203': 'Design of Experiments',
        '204': 'Statistical Computing',
        '205': 'Sampling Theory',
        '206': 'Time Series Analysis',
        '207': 'Multivariate Analysis',
        '300': 'Probability II',
        '301': 'Statistical Inference II',
        '302': 'Non-parametric Methods',
        '303': 'Bayesian Statistics',
        '304': 'Stochastic Processes',
        '305': 'Quality Control',
        '306': 'Operations Research',
        '307': 'Demographic Statistics',
        '308': 'Statistical Genetics',
        '400': 'Advanced Statistical Methods',
        '401': 'Statistical Consulting',
        '402': 'Categorical Data Analysis',
        '403': 'Survival Analysis',
        '404': 'Statistical Learning',
        '444': 'Research Project',
    },
    # Mathematics (MAT)
    'MAT': {
        '101': 'Calculus I',
        '102': 'Calculus II',
        '103': 'Linear Algebra I',
        '104': 'Discrete Mathematics',
        '105': 'Introduction to Proofs',
        '106': 'Ordinary Differential Equations',
        '107': 'Numerical Methods',
        '108': 'Real Analysis I',
        '109': 'Abstract Algebra I',
        '110': 'Complex Analysis',
        '111': 'Partial Differential Equations',
        '112': 'Topology',
        '113': 'Functional Analysis',
        '114': 'Measure Theory',
        '115': 'Number Theory',
        '116': 'Differential Geometry',
        '124': 'Mathematical Statistics',
    },
    # Bioinformatics/Computational Biology (BCB)
    'BCB': {
        '108': 'Introduction to Bioinformatics',
    },
    # Biostatistics (BIT)
    'BIT': {
        '113': 'Biostatistics',
    },
}

# ─── Data Classes ────────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    details: List[str] = field(default_factory=list)
    severity: str = "error"  # error, warning, info

@dataclass
class VerificationReport:
    project_root: str
    checks: List[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks if c.severity == "error")

    @property
    def error_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for c in self.checks if not c.passed and c.severity == "warning")

# ─── File Discovery ──────────────────────────────────────────────

def find_code_files(root: str, extensions: List[str] = None) -> List[Path]:
    """Find all code files in the project."""
    if extensions is None:
        extensions = ['.py', '.kt', '.java', '.js', '.ts', '.go', '.rs', '.sh', '.yaml', '.yml', '.json', '.toml']

    ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.openclaw'}
    files = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(Path(dirpath) / f)

    return files

def read_file_safe(path: Path) -> Optional[str]:
    """Read file contents safely."""
    try:
        return path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None

# ─── Check: Paid API References ─────────────────────────────────

def check_paid_apis(root: str) -> CheckResult:
    """Check for references to paid APIs in code."""
    details = []
    files = find_code_files(root)
    combined_pattern = re.compile('|'.join(PAID_API_PATTERNS), re.IGNORECASE)

    for f in files:
        content = read_file_safe(f)
        if content is None:
            continue
        for i, line in enumerate(content.split('\n'), 1):
            if combined_pattern.search(line):
                details.append(f"  {f}:{i}: {line.strip()[:120]}")

    passed = len(details) == 0
    return CheckResult(
        name="Paid API References",
        passed=passed,
        message=f"Found {len(details)} paid API references" if not passed else "No paid API references found",
        details=details[:50],  # Cap at 50
        severity="error"
    )

# ─── Check: Paid Dependencies ───────────────────────────────────

def check_paid_dependencies(root: str) -> CheckResult:
    """Check for paid dependencies in package files."""
    details = []
    dep_files = ['requirements.txt', 'requirements*.txt', 'pyproject.toml', 'package.json', 'build.gradle', 'build.gradle.kts']

    dep_pattern = re.compile('|'.join(PAID_DEPENDENCY_PATTERNS), re.IGNORECASE)

    for pattern in dep_files:
        import glob
        for f in glob.glob(os.path.join(root, '**', pattern), recursive=True):
            content = read_file_safe(Path(f))
            if content and dep_pattern.search(content):
                details.append(f"  {f}: contains paid dependency reference")

    passed = len(details) == 0
    return CheckResult(
        name="Paid Dependencies",
        passed=passed,
        message=f"Found {len(details)} paid dependency references" if not passed else "No paid dependencies found",
        details=details,
        severity="error"
    )

# ─── Check: Academic Framework Completeness ─────────────────────

def check_academic_completeness(root: str) -> CheckResult:
    """Check that ALL academic degree units are mapped in the codebase."""
    details = []
    found_units = set()

    # Search for academic unit references in code
    code_files = find_code_files(root, ['.py', '.kt', '.java', '.md', '.json'])

    for f in code_files:
        content = read_file_safe(f)
        if content is None:
            continue
        # Look for unit codes like ECO101, STA200, MAT103
        for dept in ACADEMIC_UNITS:
            for code in ACADEMIC_UNITS[dept]:
                unit_id = f"{dept}{code}"
                # Check various formats
                patterns = [
                    rf'\b{dept}\s*{code}\b',
                    rf'\b{unit_id}\b',
                    rf'"{unit_id}"',
                    rf"'{unit_id}'",
                    rf'{dept.lower()}{code}',
                ]
                for pat in patterns:
                    if re.search(pat, content, re.IGNORECASE):
                        found_units.add(unit_id)
                        break

    total_units = sum(len(codes) for codes in ACADEMIC_UNITS.values())
    missing_units = []

    for dept, codes in ACADEMIC_UNITS.items():
        for code in codes:
            unit_id = f"{dept}{code}"
            if unit_id not in found_units:
                missing_units.append(f"  {unit_id}: {ACADEMIC_UNITS[dept][code]}")

    coverage = len(found_units) / total_units * 100 if total_units > 0 else 0
    passed = coverage >= 95  # Allow 5% tolerance

    return CheckResult(
        name="Academic Framework Completeness",
        passed=passed,
        message=f"Coverage: {coverage:.1f}% ({len(found_units)}/{total_units} units mapped)",
        details=missing_units[:30],
        severity="warning" if coverage >= 80 else "error"
    )

# ─── Check: PQC Stub Flags ──────────────────────────────────────

def check_pqc_stubs(root: str) -> CheckResult:
    """Check that Post-Quantum Cryptography stubs are present."""
    details = []
    pqc_keywords = ['pqc', 'post-quantum', 'kyber', 'dilithium', 'sphincs', 'falcon', 'lattice', 'ntru']
    code_files = find_code_files(root, ['.py', '.kt', '.java'])

    found_pqc = False
    for f in code_files:
        content = read_file_safe(f)
        if content is None:
            continue
        content_lower = content.lower()
        for kw in pqc_keywords:
            if kw in content_lower:
                found_pqc = True
                details.append(f"  {f}: contains '{kw}' reference")
                break

    # Also check for PQC stub patterns
    stub_patterns = [
        r'pqc.*stub',
        r'stub.*pqc',
        r'post.quantum.*stub',
        r'ENABLE_PQC',
        r'PQC_ENABLED',
        r'use_pqc',
    ]

    for f in code_files:
        content = read_file_safe(f)
        if content is None:
            continue
        for pat in stub_patterns:
            if re.search(pat, content, re.IGNORECASE):
                found_pqc = True
                details.append(f"  {f}: has PQC stub flag")

    return CheckResult(
        name="PQC Stub Presence",
        passed=found_pqc,
        message="PQC stubs found" if found_pqc else "No PQC stubs found — consider adding",
        details=list(set(details))[:20],
        severity="warning"
    )

# ─── Check: Syntax Validity ─────────────────────────────────────

def check_syntax(root: str) -> CheckResult:
    """Check Python files for syntax errors."""
    details = []
    py_files = find_code_files(root, ['.py'])

    for f in py_files:
        content = read_file_safe(f)
        if content is None:
            continue
        try:
            compile(content, str(f), 'exec')
        except SyntaxError as e:
            details.append(f"  {f}:{e.lineno}: {e.msg}")

    passed = len(details) == 0
    return CheckResult(
        name="Python Syntax",
        passed=passed,
        message=f"Found {len(details)} syntax errors" if not passed else "All Python files have valid syntax",
        details=details[:20],
        severity="error"
    )

# ─── Check: File Content Verification ───────────────────────────

def check_file_contents(root: str, min_lines: int = 5) -> CheckResult:
    """Check that reported files actually have meaningful content."""
    details = []
    code_files = find_code_files(root)

    empty_or_trivial = 0
    for f in code_files:
        content = read_file_safe(f)
        if content is None:
            continue
        lines = [l for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        if len(lines) < min_lines:
            empty_or_trivial += 1
            details.append(f"  {f}: only {len(lines)} non-comment lines")

    passed = empty_or_trivial == 0
    return CheckResult(
        name="File Content Verification",
        passed=passed,
        message=f"{empty_or_trivial} files have trivial content" if not passed else "All files have meaningful content",
        details=details[:20],
        severity="warning"
    )

# ─── Check: Test Coverage ───────────────────────────────────────

def check_test_coverage(root: str) -> CheckResult:
    """Check that test files exist for source files."""
    details = []
    src_files = find_code_files(root, ['.py'])
    test_files = [f for f in src_files if 'test' in f.name.lower() or 'test' in str(f).lower()]
    src_only = [f for f in src_files if f not in test_files]

    modules_without_tests = []
    for src in src_only:
        if src.name.startswith('__'):
            continue
        # Check if a test file exists for this module
        stem = src.stem
        has_test = any(stem in t.name for t in test_files)
        if not has_test and 'test' not in stem:
            modules_without_tests.append(f"  {src}")

    if modules_without_tests:
        details = modules_without_tests[:20]

    ratio = (len(src_only) - len(modules_without_tests)) / max(len(src_only), 1) * 100
    passed = ratio >= 50  # At least 50% coverage

    return CheckResult(
        name="Test Coverage (Basic)",
        passed=passed,
        message=f"Test coverage: {ratio:.0f}% ({len(test_files)} test files for {len(src_only)} source files)",
        details=details,
        severity="warning"
    )

# ─── Check: Paid Cloud Services ─────────────────────────────────

def check_cloud_services(root: str) -> CheckResult:
    """Check for references to paid cloud services."""
    details = []
    files = find_code_files(root)
    cloud_pattern = re.compile('|'.join(PAID_SERVICE_PATTERNS), re.IGNORECASE)

    for f in files:
        content = read_file_safe(f)
        if content is None:
            continue
        for i, line in enumerate(content.split('\n'), 1):
            if cloud_pattern.search(line):
                details.append(f"  {f}:{i}: {line.strip()[:120]}")

    passed = len(details) == 0
    return CheckResult(
        name="Paid Cloud Services",
        passed=passed,
        message=f"Found {len(details)} paid cloud service references" if not passed else "No paid cloud services referenced",
        details=details[:30],
        severity="error"
    )

# ─── Main ────────────────────────────────────────────────────────

def run_verification(root: str, checks: str = "all") -> VerificationReport:
    """Run all verification checks."""
    report = VerificationReport(project_root=root)

    check_map = {
        'cost': [check_paid_apis, check_paid_dependencies, check_cloud_services],
        'academic': [check_academic_completeness],
        'pqc': [check_pqc_stubs],
        'syntax': [check_syntax],
        'tests': [check_test_coverage],
        'content': [check_file_contents],
    }

    if checks == 'all':
        all_checks = []
        for v in check_map.values():
            all_checks.extend(v)
    else:
        all_checks = []
        for key in checks.split(','):
            key = key.strip()
            if key in check_map:
                all_checks.extend(check_map[key])

    for check_func in all_checks:
        print(f"  Running: {check_func.__name__.replace('check_', '').replace('_', ' ').title()}...")
        result = check_func(root)
        report.checks.append(result)

    return report

def print_report(report: VerificationReport):
    """Print verification report."""
    print("\n" + "=" * 70)
    print("🛡️  VERIFICATION REPORT")
    print(f"   Project: {report.project_root}")
    print("=" * 70)

    for check in report.checks:
        icon = "✅" if check.passed else ("⚠️" if check.severity == "warning" else "❌")
        print(f"\n{icon} {check.name}")
        print(f"   {check.message}")
        if check.details:
            for d in check.details[:10]:
                print(f"   {d}")
            if len(check.details) > 10:
                print(f"   ... and {len(check.details) - 10} more")

    print("\n" + "=" * 70)
    if report.passed:
        print("✅ ALL CHECKS PASSED")
    else:
        print(f"❌ VERIFICATION FAILED: {report.error_count} errors, {report.warning_count} warnings")
    print("=" * 70 + "\n")

    return 0 if report.passed else 1

def main():
    parser = argparse.ArgumentParser(description="🛡️ Code Verification Script")
    parser.add_argument('--project-root', '--root', '-r', default='.', help='Project root directory')
    parser.add_argument('--checks', '-c', default='all',
                       help='Checks to run: all, cost, academic, pqc, syntax, tests, content (comma-separated)')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    root = os.path.abspath(args.project_root)
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"🛡️ Running verification on: {root}")
    print(f"   Checks: {args.checks}")

    report = run_verification(root, args.checks)

    if args.json:
        output = {
            'project_root': report.project_root,
            'passed': report.passed,
            'error_count': report.error_count,
            'warning_count': report.warning_count,
            'checks': [
                {
                    'name': c.name,
                    'passed': c.passed,
                    'message': c.message,
                    'details': c.details,
                    'severity': c.severity,
                }
                for c in report.checks
            ]
        }
        print(json.dumps(output, indent=2))
        sys.exit(0 if report.passed else 1)
    else:
        sys.exit(print_report(report))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
🛡️ Academic Completeness Checker — Prevention System #4

Verifies ALL 42+ degree units are mapped in the codebase.
Reads actual file contents and checks for unit references.

Usage:
    python academic_completeness.py --root /path/to/project
    python academic_completeness.py --root . --report markdown
    python academic_completeness.py --root . --report json
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Set, List, Optional

# ─── Complete Academic Framework (42+ Units) ─────────────────────

DEGREE_UNITS = {
    'ECONOMICS': {
        'ECO100': 'Introduction to Economics',
        'ECO101': 'Microeconomics I',
        'ECO102': 'Macroeconomics I',
        'ECO200': 'Intermediate Microeconomics',
        'ECO201': 'Intermediate Macroeconomics',
        'ECO202': 'Mathematical Economics',
        'ECO203': 'Econometrics I',
        'ECO204': 'Development Economics',
        'ECO205': 'International Economics',
        'ECO206': 'Public Finance',
        'ECO207': 'Money and Banking',
        'ECO208': 'Agricultural Economics',
        'ECO300': 'Advanced Microeconomics',
        'ECO301': 'Advanced Macroeconomics',
        'ECO302': 'Econometrics II',
        'ECO303': 'Economics of Planning',
        'ECO304': 'Labor Economics',
        'ECO305': 'Environmental Economics',
        'ECO306': 'Health Economics',
        'ECO307': 'Economics of Education',
        'ECO308': 'Industrial Organization',
        'ECO309': 'Transport Economics',
        'ECO400': 'Advanced Econometrics',
        'ECO401': 'Economic Policy Analysis',
        'ECO402': 'Game Theory',
        'ECO403': 'Behavioral Economics',
        'ECO404': 'Financial Economics',
        'ECO424': 'Research Project (Economics)',
    },
    'STATISTICS': {
        'STA142': 'Introduction to Probability',
        'STA143': 'Introduction to Statistics',
        'STA200': 'Probability I',
        'STA201': 'Statistical Inference I',
        'STA202': 'Regression Analysis',
        'STA203': 'Design of Experiments',
        'STA204': 'Statistical Computing',
        'STA205': 'Sampling Theory',
        'STA206': 'Time Series Analysis',
        'STA207': 'Multivariate Analysis',
        'STA300': 'Probability II',
        'STA301': 'Statistical Inference II',
        'STA302': 'Non-parametric Methods',
        'STA303': 'Bayesian Statistics',
        'STA304': 'Stochastic Processes',
        'STA305': 'Quality Control',
        'STA306': 'Operations Research',
        'STA307': 'Demographic Statistics',
        'STA308': 'Statistical Genetics',
        'STA400': 'Advanced Statistical Methods',
        'STA401': 'Statistical Consulting',
        'STA402': 'Categorical Data Analysis',
        'STA403': 'Survival Analysis',
        'STA404': 'Statistical Learning',
        'STA444': 'Research Project (Statistics)',
    },
    'MATHEMATICS': {
        'MAT101': 'Calculus I',
        'MAT102': 'Calculus II',
        'MAT103': 'Linear Algebra I',
        'MAT104': 'Discrete Mathematics',
        'MAT105': 'Introduction to Proofs',
        'MAT106': 'Ordinary Differential Equations',
        'MAT107': 'Numerical Methods',
        'MAT108': 'Real Analysis I',
        'MAT109': 'Abstract Algebra I',
        'MAT110': 'Complex Analysis',
        'MAT111': 'Partial Differential Equations',
        'MAT112': 'Topology',
        'MAT113': 'Functional Analysis',
        'MAT114': 'Measure Theory',
        'MAT115': 'Number Theory',
        'MAT116': 'Differential Geometry',
        'MAT124': 'Mathematical Statistics',
    },
    'INTERDISCIPLINARY': {
        'BCB108': 'Introduction to Bioinformatics',
        'BIT113': 'Biostatistics',
    },
}

def get_all_units() -> Dict[str, str]:
    """Flatten all units into a single dict."""
    all_units = {}
    for dept_units in DEGREE_UNITS.values():
        all_units.update(dept_units)
    return all_units


def find_relevant_files(root: str) -> List[Path]:
    """Find files that might contain academic framework mappings."""
    extensions = {'.py', '.kt', '.java', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.txt'}
    ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
    files = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for f in filenames:
            if any(f.endswith(ext) for ext in extensions):
                files.append(Path(dirpath) / f)

    return files


def search_unit_in_content(content: str, unit_id: str, unit_name: str) -> bool:
    """Search for a unit reference in file content using multiple patterns."""
    # Normalize unit ID for flexible matching
    dept = re.match(r'([A-Z]+)', unit_id).group(1)
    code = unit_id[len(dept):]

    patterns = [
        # Exact matches
        rf'\b{unit_id}\b',                          # ECO101
        rf'\b{dept}\s*{code}\b',                     # ECO 101
        rf'"{unit_id}"',                             # "ECO101"
        rf"'{unit_id}'",                             # 'ECO101'
        # Case-insensitive
        rf'\b{dept.lower()}{code}\b',                # eco101
        rf'\b{dept}{code.lower()}\b',                # ECO101
        # Name references
        rf'\b{re.escape(unit_name)}\b',              # Full name
        # JSON/YAML keys
        rf'"{unit_id}"\s*:',                         # "ECO101":
        rf'{unit_id}\s*:',                           # ECO101:
        # Array/list entries
        rf'\[\s*"{unit_id}"',                        # ["ECO101"
        rf'"{unit_id}"\s*,',                         # "ECO101",
        # Variable names
        rf'{dept}_{code}',                           # ECO_101
        rf'{dept.lower()}_{code}',                   # eco_101
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False


def check_completeness(root: str) -> Dict:
    """Check academic framework completeness."""
    all_units = get_all_units()
    total_units = len(all_units)

    found_units: Set[str] = set()
    unit_locations: Dict[str, List[str]] = {}  # unit -> [files where found]

    files = find_relevant_files(root)

    for filepath in files:
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue

        for unit_id, unit_name in all_units.items():
            if search_unit_in_content(content, unit_id, unit_name):
                found_units.add(unit_id)
                if unit_id not in unit_locations:
                    unit_locations[unit_id] = []
                unit_locations[unit_id].append(str(filepath))

    missing_units = {uid: uname for uid, uname in all_units.items() if uid not in found_units}

    # Group missing by department
    missing_by_dept = {}
    for unit_id, unit_name in missing_units.items():
        dept = re.match(r'([A-Z]+)', unit_id).group(1)
        if dept not in missing_by_dept:
            missing_by_dept[dept] = []
        missing_by_dept[dept].append((unit_id, unit_name))

    coverage = len(found_units) / total_units * 100 if total_units > 0 else 0

    return {
        'total_units': total_units,
        'found_units': len(found_units),
        'missing_units': len(missing_units),
        'coverage_percent': round(coverage, 1),
        'found': sorted(found_units),
        'missing': missing_units,
        'missing_by_department': missing_by_dept,
        'locations': unit_locations,
    }


def print_report(result: Dict, format: str = 'text'):
    """Print the completeness report."""
    if format == 'json':
        print(json.dumps(result, indent=2))
        return

    if format == 'markdown':
        print("# Academic Framework Completeness Report\n")
        print(f"**Total Units:** {result['total_units']}")
        print(f"**Found:** {result['found_units']} ({result['coverage_percent']}%)")
        print(f"**Missing:** {result['missing_units']}")
        print()

        if result['missing_by_department']:
            print("## Missing Units\n")
            for dept, units in result['missing_by_department'].items():
                print(f"### {dept}")
                for uid, uname in units:
                    print(f"- `{uid}`: {uname}")
                print()
        else:
            print("## ✅ All Units Mapped!\n")

        return

    # Text format
    print("\n" + "=" * 60)
    print("🎓 ACADEMIC FRAMEWORK COMPLETENESS CHECK")
    print("=" * 60)
    print(f"\n  Total Units:    {result['total_units']}")
    print(f"  Found:          {result['found_units']} ({result['coverage_percent']}%)")
    print(f"  Missing:        {result['missing_units']}")

    if result['missing_by_department']:
        print("\n  MISSING UNITS:")
        for dept, units in result['missing_by_department'].items():
            print(f"\n  {dept}:")
            for uid, uname in units:
                print(f"    ❌ {uid}: {uname}")
    else:
        print("\n  ✅ ALL UNITS MAPPED!")

    print("\n" + "=" * 60)

    if result['coverage_percent'] >= 95:
        print("✅ PASS: Academic framework is sufficiently complete")
    elif result['coverage_percent'] >= 80:
        print("⚠️  WARNING: Academic framework is mostly complete but has gaps")
    else:
        print("❌ FAIL: Academic framework has significant gaps")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="🎓 Academic Completeness Checker")
    parser.add_argument('--root', '-r', default='.', help='Project root directory')
    parser.add_argument('--report', '-f', choices=['text', 'json', 'markdown'], default='text', help='Report format')
    parser.add_argument('--strict', action='store_true', help='Fail if < 100% coverage')
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"🎓 Checking academic completeness in: {root}\n")
    result = check_completeness(root)
    print_report(result, args.report)

    if args.strict:
        sys.exit(0 if result['coverage_percent'] >= 100 else 1)
    else:
        sys.exit(0 if result['coverage_percent'] >= 95 else 1)


if __name__ == '__main__':
    main()

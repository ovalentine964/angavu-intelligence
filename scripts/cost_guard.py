#!/usr/bin/env python3
"""
🛡️ Cost Guard — Prevention System #3

Pre-commit hook that blocks paid APIs, non-free dependencies, and costly cloud services.
Run before every commit to enforce zero-cost mandate.

Usage:
    # As pre-commit hook:
    python cost_guard.py --staged          # Check only staged files
    python cost_guard.py                   # Check all files
    python cost_guard.py --install-hook    # Install as git pre-commit hook
"""

import os
import re
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple

# ─── Blocked Patterns ────────────────────────────────────────────

BLOCKED_APIS = {
    'OpenAI': [
        r'import\s+openai',
        r'from\s+openai',
        r'openai\.ChatCompletion',
        r'openai\.chat\.completions',
        r'client\s*=\s*OpenAI',
        r'api\.openai\.com',
        r'OPENAI_API_KEY',
        r'gpt-4',
        r'gpt-3\.5',
        r'gpt-4o',
        r'o1-preview',
        r'o1-mini',
    ],
    'Anthropic': [
        r'import\s+anthropic',
        r'from\s+anthropic',
        r'client\s*=\s*Anthropic',
        r'api\.anthropic\.com',
        r'ANTHROPIC_API_KEY',
        r'claude-3',
        r'claude-2',
        r'claude-instant',
    ],
    'Google (paid)': [
        r'import\s+google\.generativeai',
        r'from\s+google\.generativeai',
        r'gemini-pro',
        r'gemini-ultra',
        r'GOOGLE_API_KEY',
        r'GOOGLE_GENERATIVE_AI_KEY',
        r'generativelanguage\.googleapis',
    ],
    'DeepSeek (paid)': [
        r'api\.deepseek\.com',
        r'DEEPSEEK_API_KEY',
        r'deepseek\.ChatCompletion',
    ],
    'Cohere': [
        r'import\s+cohere',
        r'from\s+cohere',
        r'COHERE_API_KEY',
        r'api\.cohere\.ai',
    ],
    'Mistral (paid)': [
        r'api\.mistral\.ai',
        r'MISTRAL_API_KEY',
        r'import\s+mistralai',
    ],
    'Perplexity': [
        r'api\.perplexity\.ai',
        r'PERPLEXITY_API_KEY',
    ],
}

BLOCKED_DEPENDENCIES = [
    r'^openai',
    r'^anthropic',
    r'^google-generativeai',
    r'^cohere',
    r'^mistralai',
    r'^perplexity',
]

BLOCKED_CLOUD_SERVICES = [
    r'aws\.amazon\.com',
    r'console\.cloud\.google',
    r'portal\.azure\.com',
    r'\.amazonaws\.com',
    r'\.googleapis\.com(?!/storage)',
    r'\.azure\.com',
    r'\.firebase\.io',
    r'\.firebaseio\.com',
    r'supabase\.co',
    r'planetscale\.com',
    r'neon\.tech',
    r'vercel\.com',
    r'netlify\.com',
]

BLOCKED_CONFIG_PATTERNS = [
    # API keys in config files
    r'["\']api_key["\'].*["\']sk-',
    r'["\']token["\'].*["\']sk-',
    r'["\']secret["\'].*["\']sk-',
    r'api[_-]?key\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
]

# ─── File Scanning ───────────────────────────────────────────────

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
CODE_EXTENSIONS = {'.py', '.kt', '.java', '.js', '.ts', '.go', '.rs', '.sh', '.yaml', '.yml', '.json', '.toml', '.env', '.cfg', '.ini', '.md'}


def get_staged_files() -> List[str]:
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True, check=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_all_files(root: str) -> List[str]:
    """Get all code files in the project."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            if any(f.endswith(ext) for ext in CODE_EXTENSIONS):
                files.append(os.path.join(dirpath, f))
    return files


def read_file(path: str) -> str:
    """Read file contents safely."""
    try:
        return Path(path).read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''

# ─── Violation Detection ─────────────────────────────────────────

def scan_file(filepath: str, content: str) -> List[Tuple[str, str, int, str]]:
    """
    Scan a file for cost violations.
    Returns: [(category, pattern_name, line_number, line_content), ...]
    """
    violations = []

    for service, patterns in BLOCKED_APIS.items():
        for pattern in patterns:
            for i, line in enumerate(content.split('\n'), 1):
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append(('Paid API', service, i, line.strip()[:120]))

    for pattern in BLOCKED_CLOUD_SERVICES:
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(pattern, line, re.IGNORECASE):
                # Allow documentation references
                if any(word in line.lower() for word in ['example', 'documentation', 'docs', 'readme', 'note:', 'todo:']):
                    continue
                violations.append(('Paid Service', 'Cloud', i, line.strip()[:120]))

    for pattern in BLOCKED_CONFIG_PATTERNS:
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(pattern, line, re.IGNORECASE):
                violations.append(('API Key', 'Hardcoded key', i, line.strip()[:120]))

    return violations


def scan_dependencies(filepath: str, content: str) -> List[Tuple[str, str, int, str]]:
    """Scan dependency files for paid packages."""
    violations = []
    if not any(filepath.endswith(ext) for ext in ['requirements.txt', 'pyproject.toml', 'package.json', 'build.gradle']):
        return violations

    for i, line in enumerate(content.split('\n'), 1):
        for pattern in BLOCKED_DEPENDENCIES:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append(('Paid Dependency', 'Package', i, line.strip()[:120]))

    return violations

# ─── Hook Installation ───────────────────────────────────────────

def install_hook():
    """Install cost_guard as a git pre-commit hook."""
    hook_dir = '.git/hooks'
    hook_path = os.path.join(hook_dir, 'pre-commit')

    if not os.path.isdir(hook_dir):
        print("Error: Not in a git repository")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    guard_path = os.path.join(script_dir, 'cost_guard.py')

    hook_content = f"""#!/bin/bash
# Cost Guard Pre-Commit Hook
# Blocks paid APIs, non-free dependencies, and costly cloud services

echo "🛡️ Running Cost Guard..."
python3 "{guard_path}" --staged
exit $?
"""

    with open(hook_path, 'w') as f:
        f.write(hook_content)
    os.chmod(hook_path, 0o755)

    print(f"✅ Cost Guard installed at {hook_path}")
    print("   Every commit will now be checked for paid API references.")

# ─── Main ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🛡️ Cost Guard — Block paid APIs and services")
    parser.add_argument('--staged', '-s', action='store_true', help='Check only staged files')
    parser.add_argument('--install-hook', '-i', action='store_true', help='Install as git pre-commit hook')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    args = parser.parse_args()

    if args.install_hook:
        install_hook()
        sys.exit(0)

    if args.staged:
        files = get_staged_files()
        if not files:
            print("✅ No staged files to check")
            sys.exit(0)
    else:
        files = get_all_files(args.root)

    all_violations = []

    for filepath in files:
        content = read_file(filepath)
        if not content:
            continue

        violations = scan_file(filepath, content)
        violations.extend(scan_dependencies(filepath, content))

        for v in violations:
            all_violations.append((filepath,) + v)

    if args.json:
        import json
        output = {
            'passed': len(all_violations) == 0,
            'violation_count': len(all_violations),
            'violations': [
                {
                    'file': v[0],
                    'category': v[1],
                    'service': v[2],
                    'line': v[3],
                    'content': v[4],
                }
                for v in all_violations
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        if all_violations:
            print("\n" + "=" * 70)
            print("❌ COST GUARD VIOLATIONS")
            print("=" * 70)

            for filepath, category, service, line, content in all_violations:
                print(f"\n  🚫 {category}: {service}")
                print(f"     File: {filepath}:{line}")
                print(f"     Code: {content}")

            print("\n" + "=" * 70)
            print(f"❌ BLOCKED: {len(all_violations)} violation(s) found")
            print("   Remove paid API references before committing.")
            print("   Use free alternatives: HuggingFace, Ollama, local models")
            print("=" * 70 + "\n")
            sys.exit(1)
        else:
            print("✅ Cost Guard: No violations found. All clear!")
            sys.exit(0)

if __name__ == '__main__':
    main()

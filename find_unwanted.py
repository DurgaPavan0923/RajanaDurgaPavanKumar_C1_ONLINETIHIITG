#!/usr/bin/env python3
"""Comprehensive Audit Script to identify unwanted, scratch, duplicate, and orphan files.

Categorizes files into:
1. Generated / Cache Files (.ipynb_checkpoints, __pycache__, *.pyc, *.log, *.tmp)
2. Duplicates and Scratch Files (hash collisions, migration scratch scripts, temp test copies)
3. Orphaned Files (stray root files in task directories, unreferenced outputs)
4. Risky Files (.env, private keys, access tokens)
5. Large Files (> 10 MB)
6. Empty Files & Directories
Cross-checks candidate files against all references across code, notebooks, and READMEs.
"""

import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Allowed repository root items
ALLOWED_ROOT_FILES = {
    ".env.example",
    ".gitignore",
    ".python-version",
    ".vercelignore",
    "Dockerfile",
    "LICENSE",
    "Makefile",
    "README.md",
    "pyproject.toml",
    "render.yaml",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-serverless.txt",
    "vercel.json",
    "main.py",
    # Official Programme Tooling & Verification Scripts
    "cleanup.sh",
    "run_all.py",
    "run_all.sh",
    "check_notebook_format.py",
    "check_tables.py",
    "find_hidden_tables.py",
    "find_unwanted.py",
    "verify_order.py",
    "rename_zero_pad.sh",
    "sync_notebook_to_py.py",
    "update_readmes.py",
    "strip_emoji.py",
}

# Directories that are ignored during general scans
IGNORED_DIRS = {".git", ".venv", "venv", ".idea", ".vscode", ".pytest_cache"}


def file_hash(path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def collect_repo_references() -> set:
    """Scan all python files, notebooks, yaml, and readmes to build reference set."""
    references = set()
    for ext in ("*.py", "*.ipynb", "*.md", "*.yaml", "*.yml", "*.json", "*.sh", "*.ps1"):
        for p in ROOT.rglob(ext):
            if any(ign in p.parts for ign in IGNORED_DIRS):
                continue
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                # Look for file names and paths
                for token in re.findall(r"[\w\-\./\\]+\.[a-zA-Z0-9_]+", content):
                    norm = token.replace("\\", "/").strip("\"' ")
                    references.add(norm)
                    references.add(Path(norm).name)
            except Exception:
                pass
    return references


def scan_unwanted():
    print("=" * 105)
    print("Repository Hygiene & File Audit: RajanaDurgaPavanKumar_C1_ONLINETIHIITG")
    print("=" * 105)

    references = collect_repo_references()

    cache_files = []
    duplicate_files = []
    orphan_files = []
    stray_root_files = []
    risky_files = []
    large_files = []
    empty_items = []

    hashes = {}

    for root, dirs, files in os.walk(ROOT):
        # Exclude git and virtual environment from unwanted scanning
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        curr_dir = Path(root)

        # Check for empty directories
        if not dirs and not files and curr_dir != ROOT:
            empty_items.append((curr_dir.relative_to(ROOT), 0, "Empty Directory"))

        for file_name in files:
            file_path = curr_dir / file_name
            rel_path = file_path.relative_to(ROOT)
            rel_str = rel_path.as_posix()
            try:
                sz = file_path.stat().st_size
            except Exception:
                sz = 0

            # 1. Risky Files
            if file_name == ".env" or file_name.endswith(".pem") or file_name.endswith(".key") or "secret" in file_name.lower():
                risky_files.append((rel_str, sz, "CRITICAL: Potential secrets/credentials file"))

            # 2. Large Files (> 10 MB)
            if sz > 10 * 1024 * 1024:
                large_files.append((rel_str, sz, f"Large file ({sz / (1024*1024):.2f} MB)"))

            # 3. Cache and Generated Files
            if (
                "__pycache__" in curr_dir.parts
                or ".ipynb_checkpoints" in curr_dir.parts
                or file_name.endswith(".pyc")
                or file_name.endswith(".pyo")
                or file_name.endswith(".tmp")
                or file_name in (".DS_Store", "Thumbs.db")
                or (file_name.endswith(".log") and "outputs/logs" in rel_str)
            ):
                cache_files.append((rel_str, sz, "Ephemeral cache / bytecode / OS artifact"))

            # 4. Empty Files (excluding .gitkeep)
            if sz == 0 and file_name != ".gitkeep":
                empty_items.append((rel_str, 0, "Empty zero-byte file"))

            # 5. Root Clutter
            if curr_dir == ROOT:
                if file_name not in ALLOWED_ROOT_FILES:
                    # Check if it's a migration scratch script or obsolete artifact
                    stray_root_files.append((rel_str, sz, "Unapproved root file (not in allowed root specification)"))

            # 6. Stray files in Day_Wise_Tasks directories (outside outputs/ and task files)
            if "Day_Wise_Tasks" in curr_dir.parts and "outputs" not in curr_dir.parts:
                # Valid task folder files: README.md, dayXX_*.ipynb, dayXX_*.py
                if not (file_name.startswith("day") or file_name == "README.md"):
                    # Check if referenced
                    is_ref = (file_name in references) or (rel_str in references)
                    reason = "Stray loose file in task directory" if not is_ref else "Legacy task artifact (referenced)"
                    if not is_ref:
                        orphan_files.append((rel_str, sz, reason))

            # 7. Duplicates by Hash
            if sz > 0 and not any(ign in curr_dir.parts for ign in IGNORED_DIRS):
                h = file_hash(file_path)
                if h in hashes:
                    orig = hashes[h]
                    duplicate_files.append((rel_str, sz, f"Exact content duplicate of {orig}"))
                else:
                    hashes[h] = rel_str

    print(f"\n1. RISKY / SECRET FILES: {len(risky_files)}")
    if risky_files:
        for p, s, r in risky_files:
            print(f"   [CRITICAL] {p:<50} ({s} bytes) -> {r}")
            print("   Action: git filter-repo --invert-paths --path <file> and rotate exposed credentials!")
    else:
        print("   None found. 0 secret or credential files detected.")

    print(f"\n2. LARGE FILES (> 10 MB): {len(large_files)}")
    if large_files:
        for p, s, r in large_files:
            print(f"   [WARN] {p:<50} -> {r}")
    else:
        print("   None found. All tracked files are within lightweight git thresholds.")

    print(f"\n3. ROOT CLUTTER / MIGRATION SCRIPTS: {len(stray_root_files)}")
    for p, s, r in stray_root_files:
        is_ref = (Path(p).name in references)
        print(f"   {p:<50} ({s} bytes) -> {r} {'[REFERENCED]' if is_ref else '[UNREFERENCED]'}")

    print(f"\n4. ORPHANED & STRAY TASK FILES: {len(orphan_files)}")
    for p, s, r in orphan_files:
        print(f"   {p:<50} ({s} bytes) -> {r}")

    print(f"\n5. DUPLICATE FILES: {len(duplicate_files)}")
    for p, s, r in duplicate_files:
        print(f"   {p:<50} ({s} bytes) -> {r}")

    print(f"\n6. CACHE & BYTECODE FILES: {len(cache_files)}")
    print(f"   Discovered {len(cache_files)} ephemeral cache files.")

    print(f"\n7. EMPTY FILES & DIRECTORIES: {len(empty_items)}")
    for p, s, r in empty_items:
        print(f"   {p} -> {r}")

    print("=" * 105)
    return {
        "risky": risky_files,
        "large": large_files,
        "root_clutter": stray_root_files,
        "orphans": orphan_files,
        "duplicates": duplicate_files,
        "cache": cache_files,
        "empty": empty_items,
    }


if __name__ == "__main__":
    scan_unwanted()

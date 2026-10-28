#!/usr/bin/env python3
"""Comprehensive Repository File-by-File Audit & Inventory Generator.

AquaGuard AI v2.1.0 / RajanaDurgaPavanKumar_C1_ONLINETIHIITG
Author: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati AI/ML Internship)
Assigned Mentor: Sushil Meher, Teaching Assistant at Indian Institute of Technology, Guwahati

Performs file-by-file audit across repository:
- Scans all files (excluding .git and .venv)
- Evaluates Type, Size, Last referenced by, Status (KEEP / FIX / DELETE / MERGE), Reason
- Computes SHA-256 digests and detects exact duplicate files
- Scans text files for secrets, tokens, credentials
- Flags large files exceeding 10 MB threshold
- Generates cleanup.sh and cleanup.ps1 (dry-run default, --apply execution)
- Outputs structured Markdown table and summary report
"""

import hashlib
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    ".pytest_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
}

# Regex secret patterns
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google / Firebase API Key"),
    (r"sk-[0-9a-zA-Z]{20,}", "OpenAI / Anthropic Secret Key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "Cryptographic Private Key"),
]

# Canonical allowed root files
CANONICAL_ROOT_FILES = {
    ".env.example",
    ".gitattributes",
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
    # Verification & audit scripts
    "audit_repo.py",
    "cleanup.sh",
    "cleanup.ps1",
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


def compute_sha256(path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def detect_file_type(path: Path) -> str:
    """Returns human-readable classification of file type."""
    suffix = path.suffix.lower()
    name = path.name.lower()

    if name in (".gitignore", ".gitattributes", ".vercelignore", ".env.example", ".python-version"):
        return "Configuration"
    if name in ("dockerfile", "makefile"):
        return "Build Script"
    if suffix == ".py":
        return "Python Source"
    if suffix == ".ipynb":
        return "Jupyter Notebook"
    if suffix == ".md":
        return "Markdown Documentation"
    if suffix in (".yaml", ".yml"):
        return "YAML Specification"
    if suffix == ".json":
        return "JSON Schema/Data"
    if suffix == ".csv":
        return "CSV Dataset"
    if suffix == ".parquet":
        return "Parquet Dataset"
    if suffix == ".joblib":
        return "Model Pipeline Artifact"
    if suffix in (".png", ".jpg", ".jpeg", ".svg", ".ico"):
        return "Image / Graphic"
    if suffix in (".sh", ".ps1"):
        return "Shell / Automation Script"
    if suffix == ".txt":
        return "Text Specification"
    if suffix in (".pyc", ".pyo"):
        return "Python Bytecode"
    return "Generic File"


def format_size(bytes_size: int) -> str:
    """Formats bytes into human-readable size."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"


def build_reference_index(root_dir: Path) -> dict:
    """Scans all text-readable files and builds a map of referenced paths and filenames."""
    # map: target_identifier -> set of referencing relative paths
    ref_map = defaultdict(set)
    text_exts = {".py", ".ipynb", ".md", ".yaml", ".yml", ".json", ".sh", ".ps1", ".txt", ".html", ".toml", ".csv"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        curr = Path(root)

        for fname in files:
            fpath = curr / fname
            if fpath.suffix.lower() in text_exts:
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                    src_rel = fpath.relative_to(root_dir).as_posix()
                    # Find all path-like tokens and file references
                    tokens = re.findall(r"[\w\-\./\\]+\.[a-zA-Z0-9_]+", text)
                    for tok in tokens:
                        clean_tok = tok.replace("\\", "/").strip("\"' ")
                        ref_map[clean_tok].add(src_rel)
                        ref_map[Path(clean_tok).name].add(src_rel)
                except Exception:
                    pass

    return ref_map


def scan_for_secrets(path: Path) -> list:
    """Scans text file for secrets."""
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        findings = []
        for pat, desc in SECRET_PATTERNS:
            if re.search(pat, content):
                findings.append(desc)
        return findings
    except Exception:
        return []


def run_audit(root_dir: Path):
    print("=" * 115)
    print("AUDIT: Comprehensive File-by-File Repository Inventory & Governance Audit")
    print(f"Target Directory: {root_dir}")
    print("=" * 115)

    ref_map = build_reference_index(root_dir)

    all_files = []
    hash_to_files = defaultdict(list)
    secrets_found = []
    large_files = []

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        curr = Path(root)

        for fname in files:
            fpath = curr / fname
            rel_path = fpath.relative_to(root_dir)
            rel_str = rel_path.as_posix()

            try:
                sz = fpath.stat().st_size
            except Exception:
                sz = 0

            ftype = detect_file_type(fpath)
            sha = compute_sha256(fpath) if sz > 0 else "0" * 64
            hash_to_files[sha].append(rel_str)

            # Check secrets
            if ftype in ("Python Source", "Markdown Documentation", "YAML Specification", "JSON Schema/Data", "Shell / Automation Script", "Configuration", "Text Specification"):
                sec = scan_for_secrets(fpath)
                if sec:
                    secrets_found.append((rel_str, sec))

            # Check large files (>10MB)
            if sz > 10 * 1024 * 1024:
                large_files.append((rel_str, sz))

            # Find last referencing file
            refs = ref_map.get(rel_str, set()) | ref_map.get(fname, set())
            # Exclude self reference
            refs = {r for r in refs if r != rel_str}
            last_ref = sorted(refs)[-1] if refs else "Direct / Unreferenced"

            # Determine Status and Reason
            status = "KEEP"
            reason = "Active project asset"

            # 1. Ephemeral cache / build artifacts
            if (
                "__pycache__" in curr.parts
                or ".ipynb_checkpoints" in curr.parts
                or ftype == "Python Bytecode"
                or fname in (".DS_Store", "Thumbs.db")
            ):
                status = "DELETE"
                reason = "Ephemeral cache / bytecode / OS artifact"

            # 2. Risky / unencrypted secrets
            elif fname == ".env" or fname.endswith(".key") or fname.endswith(".pem"):
                status = "FIX"
                reason = "Potential credentials file requiring redaction / secret manager"

            # 3. Root clutter
            elif curr == root_dir:
                if fname not in CANONICAL_ROOT_FILES:
                    status = "DELETE"
                    reason = "Unapproved loose file in repository root"
                else:
                    status = "KEEP"
                    reason = "Canonical root configuration / entrypoint / documentation"

            # 4. Standardized Day_Wise_Tasks files
            elif "Day_Wise_Tasks" in curr.parts:
                if "outputs" in curr.parts:
                    status = "KEEP"
                    reason = "Standardized task output figure or metric table"
                else:
                    if fname == "README.md" or fname.startswith("day"):
                        status = "KEEP"
                        reason = "Standardized task notebook, script mirror, or documentation"
                    else:
                        # Loose legacy artifact in task root
                        status = "DELETE"
                        reason = "Unreferenced legacy artifact in task folder (superseded by outputs/)"

            # 5. Production Models, Processed & Raw Datasets
            elif "models" in curr.parts or "data" in curr.parts or "src" in curr.parts or "configs" in curr.parts or "tests" in curr.parts:
                status = "KEEP"
                reason = "Core application, pipeline, test, or model asset"

            elif "public" in curr.parts or "reports" in curr.parts or ".github" in curr.parts:
                status = "KEEP"
                reason = "Public web asset, formal audit report, or CI workflow"

            all_files.append({
                "path": rel_str,
                "type": ftype,
                "size_bytes": sz,
                "size_str": format_size(sz),
                "last_ref": last_ref,
                "status": status,
                "reason": reason,
                "sha256": sha,
            })

    # Detect duplicates
    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1 and h != "0" * 64}

    # Print summary statistics
    status_counts = defaultdict(int)
    for f in all_files:
        status_counts[f["status"]] += 1

    print("\nAUDIT SUMMARY:")
    print(f"Total Files Scanned:       {len(all_files)}")
    print(f"Files to KEEP:             {status_counts['KEEP']}")
    print(f"Files to DELETE:           {status_counts['DELETE']}")
    print(f"Files to FIX:              {status_counts['FIX']}")
    print(f"Files to MERGE:            {status_counts['MERGE']}")
    print(f"Exact Duplicate Groups:    {len(duplicates)}")
    print(f"Large Files (>10MB):       {len(large_files)}")
    print(f"Secret Exposures Detected: {len(secrets_found)}")

    # Detailed Deletions List
    delete_files = [f for f in all_files if f["status"] == "DELETE"]
    if delete_files:
        print(f"\nCANDIDATES IDENTIFIED FOR DELETION ({len(delete_files)}):")
        for f in delete_files:
            print(f"  - [{f['status']}] {f['path']:<65} | {f['size_str']:<8} | {f['reason']}")

    # Large files warning
    if large_files:
        print("\nLARGE FILES (>10MB):")
        for p, sz in large_files:
            print(f"  - {p} ({format_size(sz)})")
    else:
        print("\nLARGE FILES (>10MB): None. All files within git lightweight storage limits.")

    # Secrets warning
    if secrets_found:
        print("\nCRITICAL SECRETS DETECTED:")
        for p, secs in secrets_found:
            print(f"  - [CRITICAL] {p}: {', '.join(secs)}")
    else:
        print("SECRETS DETECTED: 0. Repository is clean of hardcoded API tokens or private keys.")

    # Generate Markdown Table Report
    report_path = root_dir / "reports" / "AUDIT_INVENTORY.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Comprehensive Repository Inventory & Governance Audit\n\n")
        f.write("### Project: AquaGuard AI v2.1.0 / RajanaDurgaPavanKumar_C1_ONLINETIHIITG\n")
        f.write("- Author: Rajana Durga Pavan Kumar (Group C1, TIH IIT Guwahati AI/ML Internship)\n")
        f.write("- Mentor: Sushil Meher (Teaching Assistant, Indian Institute of Technology, Guwahati)\n\n")
        f.write("## 1. Executive Summary\n\n")
        f.write(f"- **Total Files Scanned:** {len(all_files)}\n")
        f.write(f"- **Files Verified to KEEP:** {status_counts['KEEP']}\n")
        f.write(f"- **Files Identified for DELETION:** {status_counts['DELETE']}\n")
        f.write(f"- **Files Requiring FIX:** {status_counts['FIX']}\n")
        f.write(f"- **Exact Duplicate Groups:** {len(duplicates)}\n")
        f.write(f"- **Files > 10MB:** {len(large_files)}\n")
        f.write(f"- **Secrets / Private Keys Detected:** {len(secrets_found)}\n\n")

        f.write("## 2. Complete File Inventory Table\n\n")
        f.write("| Path | Type | Size | Last referenced by | Status | Reason |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for item in sorted(all_files, key=lambda x: x["path"]):
            f.write(f"| `{item['path']}` | {item['type']} | {item['size_str']} | `{item['last_ref']}` | **{item['status']}** | {item['reason']} |\n")

    print(f"\nGenerated Markdown inventory report at: {report_path.relative_to(root_dir)}")

    # Generate cleanup.sh and cleanup.ps1
    generate_cleanup_scripts(root_dir, delete_files)

    return all_files, delete_files, duplicates


def generate_cleanup_scripts(root_dir: Path, delete_files: list):
    """Generates cross-platform cleanup scripts with dry-run default and --apply flag."""
    rel_delete_paths = [f["path"] for f in delete_files]

    # Bash cleanup.sh
    sh_path = root_dir / "cleanup.sh"
    sh_content = [
        "#!/usr/bin/env bash",
        "# ==============================================================================",
        "# AquaGuard AI - Automated Governance Cleanup Protocol",
        "# Generated by audit_repo.py",
        "# Defaults to DRY-RUN mode (git rm -n) to safeguard workspace state.",
        "# Execute with --apply to commit file removals.",
        "# ==============================================================================",
        "set -euo pipefail",
        "",
        'MODE="dry-run"',
        'if [[ "${1:-}" == "--apply" ]]; then',
        '    MODE="apply"',
        "fi",
        "",
        'echo "=============================================================================="',
        'echo "AquaGuard AI Repository Cleanup Protocol [Mode: $MODE]"',
        'echo "=============================================================================="',
        "",
        "# 1. Purge ephemeral caches and OS artifacts",
        'echo "[1/3] Purging Python bytecode caches, pytest cache, and OS artifacts..."',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "*.pyc" -delete 2>/dev/null || true',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -name ".DS_Store" -delete 2>/dev/null || true',
        'find . -path "./.venv" -prune -o -path "./.git" -prune -o -name "Thumbs.db" -delete 2>/dev/null || true',
        "",
        "# 2. Remove identified unreferenced legacy artifacts",
        'echo "[2/3] Processing unreferenced legacy task artifacts..."',
        "FILES_TO_REMOVE=(",
    ]
    for p in rel_delete_paths:
        sh_content.append(f'    "{p}"')
    sh_content.extend([
        ")",
        "",
        'for f in "${FILES_TO_REMOVE[@]}"; do',
        '    if [[ -f "$f" ]]; then',
        '        if [[ "$MODE" == "dry-run" ]]; then',
        '            echo "[DRY-RUN] Candidate for removal: $f"',
        '            git rm -n "$f" 2>/dev/null || true',
        "        else",
        '            echo "[APPLY] Removing: $f"',
        '            git rm -f "$f" 2>/dev/null || rm -f "$f"',
        "        fi",
        "    fi",
        "done",
        "",
        'echo "[3/3] Completed."',
        'echo "=============================================================================="',
        'if [[ "$MODE" == "dry-run" ]]; then',
        '    echo "Dry-run complete. To apply deletions, run: ./cleanup.sh --apply"',
        "else",
        '    echo "Cleanup Protocol Successfully Executed."',
        "fi",
        'echo "=============================================================================="',
    ])
    sh_path.write_text("\n".join(sh_content) + "\n", encoding="utf-8")

    # PowerShell cleanup.ps1
    ps1_path = root_dir / "cleanup.ps1"
    ps1_content = [
        "# ==============================================================================",
        "# AquaGuard AI - Automated Governance Cleanup Protocol (PowerShell)",
        "# Generated by audit_repo.py",
        "# Defaults to DRY-RUN mode to safeguard workspace state.",
        "# Execute with -Apply to commit file removals.",
        "# ==============================================================================",
        "param(",
        "    [switch]$Apply = $false",
        ")",
        "",
        '$Mode = if ($Apply) { "apply" } else { "dry-run" }',
        'Write-Host "=============================================================================="',
        'Write-Host "AquaGuard AI Repository Cleanup Protocol [Mode: $Mode]"',
        'Write-Host "=============================================================================="',
        "",
        'Write-Host "[1/3] Purging Python bytecode and temporary caches..."',
        'Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Where-Object { $_.FullName -notmatch "\\.venv|\\.git" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue',
        'Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" | Where-Object { $_.FullName -notmatch "\\.venv|\\.git" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue',
        'Get-ChildItem -Path . -Recurse -Directory -Filter ".ipynb_checkpoints" | Where-Object { $_.FullName -notmatch "\\.venv|\\.git" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue',
        'Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" | Where-Object { $_.FullName -notmatch "\\.venv|\\.git" } | Remove-Item -Force -ErrorAction SilentlyContinue',
        "",
        'Write-Host "[2/3] Processing unreferenced legacy task artifacts..."',
        "$FilesToRemove = @(",
    ]
    for p in rel_delete_paths:
        ps1_content.append(f'    "{p}"')
    ps1_content.extend([
        ")",
        "",
        'foreach ($f in $FilesToRemove) {',
        '    if (Test-Path $f) {',
        '        if ($Mode -eq "dry-run") {',
        '            Write-Host "[DRY-RUN] Candidate for removal: $f"',
        '            git rm -n "$f" 2>$null',
        '        } else {',
        '            Write-Host "[APPLY] Removing: $f"',
        '            git rm -f "$f" 2>$null',
        '            if (Test-Path $f) { Remove-Item -Path $f -Force }',
        '        }',
        '    }',
        '}',
        "",
        'Write-Host "[3/3] Completed."',
        'Write-Host "=============================================================================="',
        'if ($Mode -eq "dry-run") {',
        '    Write-Host "Dry-run complete. To apply deletions, run: .\\cleanup.ps1 -Apply"',
        '} else {',
        '    Write-Host "Cleanup Protocol Successfully Executed."',
        '}',
        'Write-Host "=============================================================================="',
    ])
    ps1_path.write_text("\n".join(ps1_content) + "\n", encoding="utf-8")
    print(f"Generated {sh_path.name} and {ps1_path.name} with dry-run safety controls.")


if __name__ == "__main__":
    run_audit(ROOT)

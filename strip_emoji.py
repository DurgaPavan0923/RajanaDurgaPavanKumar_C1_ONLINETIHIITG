"""Strip all emojis and decorative symbols from the repository."""

import re
import sys
from pathlib import Path

try:
    import nbformat
except ImportError:
    nbformat = None

ROOT = Path(__file__).resolve().parent

# Comprehensive regex pattern matching emojis and decorative symbols
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # Symbols, pictographs, transport, supplemental
    "\U00002600-\U000027BF"  # Misc symbols, dingbats
    "\U00002300-\U000023FF"  # Misc technical
    "\U00002B00-\U00002BFF"  # Misc symbols & arrows
    "\U0000200D"              # Zero-width joiner
    "\U0000FE0E-\U0000FE0F"  # Variation selectors
    "]+",
    flags=re.UNICODE,
)

TARGET_EXTENSIONS = {
    ".py", ".ipynb", ".md", ".txt", ".json", ".yml", ".yaml", ".csv", ".toml", ".sh", ".ps1"
}

IGNORE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", "build", "dist"
}


def clean_text(text: str) -> tuple[str, int]:
    matches = len(EMOJI_PATTERN.findall(text))
    if matches == 0:
        return text, 0
    # Remove emojis
    cleaned = EMOJI_PATTERN.sub("", text)
    # Clean up double spaces in lines (excluding indentation)
    lines = cleaned.split("\n")
    cleaned_lines = []
    for line in lines:
        # Collapse multiple spaces within line text while keeping leading whitespace
        indent_len = len(line) - len(line.lstrip(" "))
        indent = line[:indent_len]
        body = line[indent_len:]
        body = re.sub(r"[ \t]{2,}", " ", body)
        # Clean empty headings: e.g. '# ', '## ', '### ' with no title
        if re.match(r"^#{1,6}\s*$", body):
            body = ""
        cleaned_lines.append(indent + body)
    return "\n".join(cleaned_lines), matches


def process_notebook(file_path: Path) -> int:
    with open(file_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    total_cleaned = 0
    for cell in nb.cells:
        # Clean cell source
        src = cell.source
        new_src, count = clean_text(src)
        if count > 0:
            cell.source = new_src
            total_cleaned += count

        # Clean text outputs if present
        if cell.cell_type == "code":
            for output in cell.get("outputs", []):
                if output.get("output_type") == "stream":
                    txt = output.get("text", "")
                    new_txt, count = clean_text(txt)
                    if count > 0:
                        output["text"] = new_txt
                        total_cleaned += count
                elif "data" in output:
                    for mime in ["text/plain", "text/html"]:
                        if mime in output["data"]:
                            val = output["data"][mime]
                            if isinstance(val, str):
                                new_val, count = clean_text(val)
                                if count > 0:
                                    output["data"][mime] = new_val
                                    total_cleaned += count
                            elif isinstance(val, list):
                                joined = "".join(val)
                                new_joined, count = clean_text(joined)
                                if count > 0:
                                    output["data"][mime] = [new_joined]
                                    total_cleaned += count

    if total_cleaned > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
    return total_cleaned


def process_text_file(file_path: Path) -> int:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return 0
    cleaned, count = clean_text(content)
    if count > 0:
        file_path.write_text(cleaned, encoding="utf-8")
    return count


def main():
    print(f"Scanning {ROOT} for emojis and decorative symbols...")
    total_files = 0
    total_removals = 0

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(ignored in path.parts for ignored in IGNORE_DIRS):
            continue
        if path.suffix.lower() not in TARGET_EXTENSIONS:
            continue

        if path.suffix.lower() == ".ipynb":
            removals = process_notebook(path)
        else:
            removals = process_text_file(path)

        if removals > 0:
            rel = path.relative_to(ROOT)
            print(f"Cleaned {rel}: removed {removals} decorative symbol(s)")
            total_files += 1
            total_removals += removals

    print("=" * 60)
    print(f"Summary: Cleaned {total_removals} symbols across {total_files} files.")
    print("=" * 60)


if __name__ == "__main__":
    main()

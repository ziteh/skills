#!/usr/bin/env python3
"""
Batch-convert files to Markdown using markitdown.

Usage:
    python3 batch_convert.py [directory] [--pattern GLOB] [--recursive]

Examples:
    python3 batch_convert.py                          # all supported files in current dir
    python3 batch_convert.py ~/Documents --pattern "*.pdf"
    python3 batch_convert.py . --pattern "*.xlsx" --recursive
"""

import argparse
import subprocess
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".zip", ".epub", ".png", ".jpg", ".jpeg", ".gif", ".webp",
}


def ensure_markitdown() -> None:
    try:
        import markitdown  # noqa: F401
    except ImportError:
        print("Installing markitdown...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markitdown[all]", "-q"])


def batch_convert(directory: Path, pattern: str | None, recursive: bool) -> None:
    ensure_markitdown()
    from markitdown import MarkItDown  # noqa: E402

    if pattern:
        glob = directory.rglob(pattern) if recursive else directory.glob(pattern)
        files = sorted(glob)
    else:
        glob_fn = directory.rglob if recursive else directory.glob
        files = sorted(
            p for ext in SUPPORTED_EXTENSIONS
            for p in glob_fn(f"*{ext}")
        )

    if not files:
        print(f"No matching files found in {directory}", file=sys.stderr)
        sys.exit(1)

    md = MarkItDown()
    ok, failed = 0, 0

    for path in files:
        out = path.with_suffix(".md")
        try:
            result = md.convert(str(path))
            out.write_text(result.text_content, encoding="utf-8")
            print(f"[OK]  {path} -> {out.name}")
            ok += 1
        except Exception as e:
            print(f"[ERR] {path}: {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {ok} converted, {failed} failed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-convert files to Markdown")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to search (default: current dir)")
    parser.add_argument("--pattern", help='Glob pattern, e.g. "*.xlsx" (default: all supported formats)')
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories recursively")
    args = parser.parse_args()

    batch_convert(Path(args.directory).expanduser().resolve(), args.pattern, args.recursive)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Convert a single file or URL to Markdown.

Usage:
    python3 convert.py <input> [-o output.md] [--ocr]
    python3 convert.py <input> --azure-endpoint URL --azure-key KEY [-o output.md]
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

VENV_DIR = Path(__file__).parent / ".venv"
VENV_PYTHON = VENV_DIR / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def _bootstrap() -> None:
    if not VENV_PYTHON.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
        subprocess.check_call([str(VENV_PYTHON), "-m", "pip", "install", "markitdown[all]", "-q"])
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)


def _ensure_ocr() -> None:
    try:
        import markitdown_ocr  # type: ignore[import]  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "markitdown-ocr", "-q"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a file or URL to Markdown")
    parser.add_argument("input", help="File path or URL to convert")
    parser.add_argument("-o", "--output", help="Output .md file (default: stdout)")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR for scanned/image content")
    parser.add_argument("--azure-endpoint", help="High-accuracy endpoint URL")
    parser.add_argument("--azure-key", help="High-accuracy API key")
    args = parser.parse_args()

    from markitdown import MarkItDown  # type: ignore[import]

    if args.ocr:
        _ensure_ocr()

    md: Any
    if args.azure_endpoint and args.azure_key:
        from azure.ai.documentintelligence import DocumentIntelligenceClient  # type: ignore[import]
        from azure.core.credentials import AzureKeyCredential  # type: ignore[import]
        client: Any = cast(Any, DocumentIntelligenceClient(args.azure_endpoint, AzureKeyCredential(args.azure_key)))
        md = cast(Any, MarkItDown(docintel_client=client))
    elif args.ocr:
        md = cast(Any, MarkItDown(enable_plugins=True))
    else:
        md = cast(Any, MarkItDown())

    text: str = cast(str, md.convert(args.input).text_content)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Saved: {args.output}")
    else:
        print(text)


if Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    _bootstrap()
else:
    main()

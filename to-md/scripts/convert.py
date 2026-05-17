#!/usr/bin/env python3
"""Convert a single file or URL to Markdown."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap  # pyright: ignore[reportMissingImports]

bootstrap.ensure(Path(__file__).parent)  # pyright: ignore[reportUnknownMemberType]

# ruff: noqa: E402
from typing import Any, cast

from markitdown import MarkItDown  # type: ignore[import]


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a file or URL to Markdown")
    parser.add_argument("input", help="File path or URL to convert")
    parser.add_argument("-o", "--output", help="Output .md file (default: stdout)")
    parser.add_argument(
        "--ocr", action="store_true", help="Enable OCR for scanned/image content"
    )
    parser.add_argument("--azure-endpoint", help="High-accuracy endpoint URL")
    parser.add_argument("--azure-key", help="High-accuracy API key")
    args = parser.parse_args()

    md: Any
    if args.azure_endpoint and args.azure_key:
        from azure.ai.documentintelligence import DocumentIntelligenceClient  # type: ignore[import]
        from azure.core.credentials import AzureKeyCredential  # type: ignore[import]

        client: Any = cast(
            Any,
            DocumentIntelligenceClient(
                args.azure_endpoint, AzureKeyCredential(args.azure_key)
            ),
        )
        md = cast(Any, MarkItDown(docintel_client=client))
    elif args.ocr:
        md = cast(Any, MarkItDown(enable_plugins=True))
    else:
        md = cast(Any, MarkItDown())

    text: str = cast(str, md.convert(args.input).text_content)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Saved: {args.output}", file=sys.stderr)
    else:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main())

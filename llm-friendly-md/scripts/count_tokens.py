#!/usr/bin/env python3
"""
Count approximate token usage.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap  # pyright: ignore[reportMissingImports]

bootstrap.ensure(Path(__file__).parent)  # pyright: ignore[reportUnknownMemberType]

# ruff: noqa: E402
import tiktoken

DEFAULT_ENCODING = "cl100k_base"
assert DEFAULT_ENCODING in tiktoken.list_encoding_names(), "Invalid default encoding"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Count approximate token and character usage for a text file."
    )
    parser.add_argument("file", help="File to count")
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        choices=tiktoken.list_encoding_names(),
        help=f"tiktoken encoding (default: {DEFAULT_ENCODING})",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.is_file():
        print(f"Error: '{path}' is not a file.", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    enc = tiktoken.get_encoding(args.encoding)
    tokens = len(enc.encode(text))
    chars = len(text)

    print(
        json.dumps(
            {
                "file": str(path.resolve()),
                "tokens": tokens,
                "chars": chars,
                "chars_per_token": round(chars / tokens, 3) if tokens > 0 else 0,
                "encoding": args.encoding,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

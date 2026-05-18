#!/usr/bin/env python3
"""Spell-check a Markdown file using spaCy tokenization, ignoring code blocks and inline code.

Output: one JSON object per line (JSONL), e.g.:
  {"line": 5, "word": "recieve", "suggestions": ["receive"]}
  {"line": 147, "word": "venv", "suggestions": ["ven", "vena", "vend", "venn", "vent"]}
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap  # pyright: ignore[reportMissingImports]

bootstrap.ensure(Path(__file__).parent)  # pyright: ignore[reportUnknownMemberType]

# ruff: noqa: E402
import spacy
from markdown_it import MarkdownIt
from spellchecker import SpellChecker

_SKIP_BLOCK = frozenset({"fence", "code_block", "html_block"})
_SKIP_INLINE = frozenset({"code_inline", "html_inline"})


def extract_text(md_source: str) -> list[tuple[int, str]]:
    """Process using the Markdown AST and output only text nodes."""
    tokens = MarkdownIt().parse(md_source)
    out: list[tuple[int, str]] = []
    for token in tokens:
        if token.type in _SKIP_BLOCK:
            continue
        if token.type != "inline" or not token.children:
            continue
        block_line = token.map[0] + 1 if token.map else 0
        for child in token.children:
            # Only process plain text nodes; skip code_inline, html_inline, images, etc.
            if child.type in _SKIP_INLINE or child.type != "text":
                continue
            if child.content.strip():
                # Inline children rarely have their own map; fall back to block line.
                line = child.map[0] + 1 if child.map else block_line
                out.append((line, child.content))
    return out


def load_wordlist(path: Path) -> list[str]:
    """Return non-empty, non-comment lines from a wordlist file."""
    return [
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def check_spelling(
    md_path: Path, language: str, extra_wordlists: list[Path] | None = None
) -> list[tuple[int, str, list[str]]]:
    """Return (line, original_word, suggestions) for each likely misspelling."""
    source = md_path.read_text(encoding="utf-8")
    nlp = spacy.blank(language)  # tokeniser only — no model download required
    spell = SpellChecker(language=language)

    # Auto-discover .wordlist alongside the MD file, then apply explicit lists.
    candidate_lists: list[Path] = []
    auto = md_path.parent / ".wordlist"
    if auto.is_file():
        candidate_lists.append(auto)
    if extra_wordlists:
        candidate_lists.extend(extra_wordlists)
    for wl in candidate_lists:
        spell.word_frequency.load_words(load_wordlist(wl))

    issues: list[tuple[int, str, list[str]]] = []
    seen: set[str] = set()  # suppress duplicate reports for the same word

    for line_no, text in extract_text(source):
        doc = nlp(text)
        for i, tok in enumerate(doc):
            if not tok.is_alpha or tok.is_stop:
                continue
            if tok.like_url or tok.like_email or tok.like_num:
                continue
            # Capitalised tokens that aren't sentence-first are likely proper nouns.
            if i > 0 and tok.text[0].isupper():
                continue
            word_lower = tok.lower_
            if word_lower in seen:
                continue
            if spell.unknown([word_lower]):
                seen.add(word_lower)
                suggestions = sorted(spell.candidates(word_lower) or [])[:5]
                issues.append((line_no, tok.text, suggestions))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Spell-check a Markdown file, skipping code blocks and inline code."
    )
    parser.add_argument("path", help="Path to the .md file")
    parser.add_argument(
        "--lang", default="en", help="Spell-check language (default: en)"
    )
    parser.add_argument(
        "--wordlist",
        action="append",
        metavar="FILE",
        help="Path to a wordlist file (one word per line, # for comments). May be repeated.",
    )
    args = parser.parse_args()

    md_path = Path(args.path)
    if not md_path.is_file() or md_path.suffix != ".md":
        print(f"error: '{md_path}' is not a valid .md file", file=sys.stderr)
        return 1

    extra = [Path(p) for p in args.wordlist] if args.wordlist else None
    issues = check_spelling(md_path, language=args.lang, extra_wordlists=extra)
    for line_no, word, suggestions in sorted(issues):
        print(
            json.dumps(
                {"line": line_no, "word": word, "suggestions": suggestions},
                indent=None,
                ensure_ascii=False,
            )
        )
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())

from pathlib import Path

from spell_check import check_spelling, extract_text, load_wordlist


# == extract text ==

def test_extract_text_plain() -> None:
    result = extract_text("Hello world")
    assert any("Hello world" in text for _, text in result)


def test_extract_text_returns_line_number() -> None:
    md = "line one\n\nline three"
    result = extract_text(md)
    line_numbers = [ln for ln, _ in result]
    assert 1 in line_numbers


def test_extract_text_skips_fenced_code() -> None:
    md = "text\n\n```python\nrecieve = 1\n```\n\nmore text"
    result = extract_text(md)
    combined = " ".join(t for _, t in result)
    assert "recieve" not in combined


def test_extract_text_skips_inline_code() -> None:
    md = "Use `recieve` to get data."
    result = extract_text(md)
    combined = " ".join(t for _, t in result)
    assert "recieve" not in combined


def test_extract_text_skips_indented_code_block() -> None:
    md = "intro\n\n    recieve = bad_word\n\noutro"
    result = extract_text(md)
    combined = " ".join(t for _, t in result)
    assert "recieve" not in combined


# == load wordlist ==

def test_load_wordlist_reads_words(tmp_path: Path) -> None:
    wl = tmp_path / "words.txt"
    wl.write_text("runtime\nkubernetes\n")
    assert load_wordlist(wl) == ["runtime", "kubernetes"]


def test_load_wordlist_lowercases(tmp_path: Path) -> None:
    wl = tmp_path / "words.txt"
    wl.write_text("Runtime\nKubernetes\n")
    assert load_wordlist(wl) == ["runtime", "kubernetes"]


def test_load_wordlist_skips_comments(tmp_path: Path) -> None:
    wl = tmp_path / "words.txt"
    wl.write_text("# this is a comment\nruntime\n")
    assert load_wordlist(wl) == ["runtime"]


def test_load_wordlist_skips_empty_lines(tmp_path: Path) -> None:
    wl = tmp_path / "words.txt"
    wl.write_text("\nruntime\n\n")
    assert load_wordlist(wl) == ["runtime"]


# == check spelling ==

def test_check_spelling_detects_misspelling(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("I recieve the package.\n")
    issues = check_spelling(md, language="en")
    words = [w for _, w, _ in issues]
    assert "recieve" in words


def test_check_spelling_no_issues_for_correct_text(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("The quick brown fox jumps over the lazy dog.\n")
    issues = check_spelling(md, language="en")
    assert issues == []


def test_check_spelling_skips_code_block(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("Example:\n\n```python\nrecieve = 1\n```\n")
    issues = check_spelling(md, language="en")
    assert all(w != "recieve" for _, w, _ in issues)


def test_check_spelling_extra_wordlist(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("Use the runtime environment.\n")
    wl = tmp_path / "custom.txt"
    wl.write_text("runtime\n")
    issues = check_spelling(md, language="en", extra_wordlists=[wl])
    assert all(w != "runtime" for _, w, _ in issues)


def test_check_spelling_auto_discovers_wordlist(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("Use the runtime environment.\n")
    (tmp_path / ".wordlist").write_text("runtime\n")
    issues = check_spelling(md, language="en")
    assert all(w != "runtime" for _, w, _ in issues)


def test_check_spelling_includes_suggestions(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("I recieve the package.\n")
    issues = check_spelling(md, language="en")
    misspelling = next((s for _, w, s in issues if w == "recieve"), None)
    assert misspelling is not None
    assert "receive" in misspelling

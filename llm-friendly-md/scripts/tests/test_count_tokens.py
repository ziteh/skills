from pathlib import Path

from count_tokens import DEFAULT_ENCODING, count_file_tokens


def test_basic_counts(tmp_path: Path) -> None:
    f = tmp_path / "doc.txt"
    f.write_text("hello world")
    result = count_file_tokens(f)
    assert isinstance(result["tokens"], int) and result["tokens"] > 0
    assert result["chars"] == len("hello world")
    assert result["encoding"] == DEFAULT_ENCODING


def test_empty_file(tmp_path: Path) -> None:
    f = tmp_path / "empty.txt"
    f.write_text("")
    result = count_file_tokens(f)
    assert result["tokens"] == 0
    assert result["chars"] == 0
    assert result["chars_per_token"] == 0


def test_chars_per_token_ratio(tmp_path: Path) -> None:
    f = tmp_path / "doc.txt"
    text = "a" * 100
    f.write_text(text)
    result = count_file_tokens(f)
    tokens = result["tokens"]
    chars = result["chars"]
    assert isinstance(tokens, int) and tokens > 0
    assert isinstance(chars, int) and chars == 100
    expected = round(chars / tokens, 3)
    assert result["chars_per_token"] == expected


def test_file_key_is_absolute(tmp_path: Path) -> None:
    f = tmp_path / "doc.txt"
    f.write_text("hello")
    result = count_file_tokens(f)
    assert Path(str(result["file"])).is_absolute()


def test_custom_encoding(tmp_path: Path) -> None:
    f = tmp_path / "doc.txt"
    f.write_text("hello world")
    result = count_file_tokens(f, encoding="p50k_base")
    assert result["encoding"] == "p50k_base"
    assert isinstance(result["tokens"], int) and result["tokens"] > 0

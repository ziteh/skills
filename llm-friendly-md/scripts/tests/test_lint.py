from pathlib import Path

import pytest

from lint import collect_md_files


def test_single_md_file(tmp_path: Path) -> None:
    f = tmp_path / "doc.md"
    f.write_text("# Hello")
    assert collect_md_files([f]) == [f]


def test_non_md_file_ignored(tmp_path: Path) -> None:
    txt = tmp_path / "notes.txt"
    txt.write_text("hello")
    assert collect_md_files([txt]) == []


def test_directory_finds_md_files(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# A")
    (tmp_path / "b.md").write_text("# B")
    (tmp_path / "c.txt").write_text("not md")
    result = collect_md_files([tmp_path])
    assert result == sorted([tmp_path / "a.md", tmp_path / "b.md"])


def test_directory_recursive(tmp_path: Path) -> None:
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "root.md").write_text("# root")
    (sub / "nested.md").write_text("# nested")
    result = collect_md_files([tmp_path])
    assert tmp_path / "root.md" in result
    assert sub / "nested.md" in result


def test_deduplicates_repeated_paths(tmp_path: Path) -> None:
    f = tmp_path / "doc.md"
    f.write_text("# Hi")
    result = collect_md_files([f, f])
    assert result.count(f) == 1


def test_nonexistent_path_is_skipped(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    missing = tmp_path / "ghost.md"
    result = collect_md_files([missing])
    assert result == []
    assert "ghost.md" in capsys.readouterr().err


def test_empty_directory_returns_empty_list(tmp_path: Path) -> None:
    assert collect_md_files([tmp_path]) == []

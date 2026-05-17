#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap  # pyright: ignore[reportMissingImports]

bootstrap.ensure(Path(__file__).parent)  # pyright: ignore[reportUnknownMemberType]


def collect_md_files(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        if target.is_file():
            if target.suffix == ".md":
                files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
        else:
            print(f"Warning: '{target}' does not exist, skipping.")
    return sorted(set(files))


def main() -> int:
    scripts = Path(__file__).parent
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    ext = ".exe" if sys.platform == "win32" else ""
    pymarkdown_bin = scripts / ".venv" / bin_dir / f"pymarkdown{ext}"
    config_file = scripts / ".pymarkdown.yaml"

    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+", help="Files or directories to check")
    args = parser.parse_args()

    md_files = collect_md_files([Path(t) for t in args.targets])
    if not md_files:
        print("No .md files found.")
        return 0

    result = subprocess.run(
        [str(pymarkdown_bin), "--strict-config", "--config", str(config_file), "scan"]
        + [str(f) for f in md_files]
    )
    if result.returncode == 0:
        print(f"All {len(md_files)} files passed.")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

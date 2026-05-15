#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path


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
    bin_dir = "Scripts" if sys.platform == "win32" else "bin"
    ext = ".exe" if sys.platform == "win32" else ""
    scripts_dir = Path(__file__).parent
    config_file = scripts_dir / ".pymarkdown.yaml"
    venv_dir = scripts_dir / ".venv"
    pymarkdown_bin = venv_dir / bin_dir / f"pymarkdown{ext}"
    if not pymarkdown_bin.exists():
        print("Setting up venv...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        pip = venv_dir / bin_dir / f"pip{ext}"
        subprocess.run(
            [str(pip), "install", "-r", str(scripts_dir / "requirements.txt")],
            check=True,
        )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "targets",
        nargs="+",
        help="Files or directories to check",
    )
    args = parser.parse_args()

    md_files = collect_md_files([Path(t) for t in args.targets])
    if not md_files:
        print("No .md files found.")
        return 0

    # Check files with pymarkdown
    result = subprocess.run(
        [str(pymarkdown_bin), "--strict-config", "--config", str(config_file), "scan"]
        + [str(f) for f in md_files]
    )
    return_code = result.returncode
    if return_code == 0:
        print(f"All {len(md_files)} files passed.")
    return return_code


if __name__ == "__main__":
    sys.exit(main())

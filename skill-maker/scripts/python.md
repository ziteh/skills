# Python Scripts

Please follow this guide when creating Python scripts.

> Keywords follow RFC 2119.

## Directory structure

```txt
skill-name/
├── SKILL.md
└── scripts/
    ├── requirements.txt
    └── script.py
```

## Dependency 

Python scripts MUST NOT assume host packages are installed.
Every skill MUST have a `requirements.txt` listing all third-party deps with pinned version ranges (e.g. `requests>=2.28.0,<3.0.0`).

Call `bootstrap.ensure(Path(__file__).parent)` at the top of every `run.py` — this creates an isolated `.venv`, installs deps, and runs weekly security audits automatically.

NEVER write bare imports like `import pandas` without first declaring it in `requirements.txt`.
NEVER instruct users to run `pip install` manually.

## bootstrap.py pattern

Every Python script in a skill MUST begin with this block:

```python
import sys
from pathlib import Path

_scripts = Path(__file__).parent
sys.path.insert(0, str(_scripts.parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap
bootstrap.ensure(_scripts)
```

`bootstrap.ensure(script_dir)` does:

- Creates `scripts/.venv` if it does not exist.
- Installs packages from `scripts/requirements.txt` if the file exists.
- Installs `pip-audit` and runs a weekly security audit.
- Re-executes the current script inside the venv if not already running there.

If the script has third-party dependencies, list them in `scripts/requirements.txt` (one package per line). Omit the file if there are no dependencies.

MUST NOT write bare `import` statements for third-party packages before calling `bootstrap.ensure()`.
MUST NOT instruct users to run `pip install` manually.

## Example

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

_scripts = Path(__file__).parent
sys.path.insert(0, str(_scripts.parent.parent.parent / "skill-maker" / "scripts"))
import bootstrap
bootstrap.ensure(_scripts)

# Third-party imports go here, AFTER bootstrap.ensure()
import requests

def main() -> int:
    ...

if __name__ == "__main__":
    sys.exit(main())
```

## Unit tests

### When to add tests

Add unit tests whenever a script contains logic that can be exercised without running the full CLI — pure functions that transform or filter data, parse input, or compute output.

Functions that only shell out to an external binary or whose entire body is `main()` argument parsing are better covered by integration tests or manual verification.

### Directory structure

```text
skill-name/
├── SKILL.md
└── scripts/
    ├── requirements.txt
    ├── script.py
    └── tests/
        ├── conftest.py
        ├── test_script.py
        └── readme.md
```

Add `pytest >= 8` to `requirements.txt` so the existing `.venv` includes it.

### conftest.py — neutralising bootstrap

All scripts call `bootstrap.ensure()` at module level. Importing them inside a test would trigger venv creation. Prevent this by pre-populating `sys.modules["bootstrap"]` with a `MagicMock` **before** any test file imports a script.

```python
# tests/conftest.py
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Prevent module-level bootstrap.ensure() from running when scripts are imported.
sys.modules["bootstrap"] = MagicMock()

# Make scripts importable by name.
sys.path.insert(0, str(Path(__file__).parent.parent))
```

pytest loads `conftest.py` before collecting any test module, so this mock is always in place in time.

### Writing tests

Import functions directly from the script module. Use pytest's built-in `tmp_path` fixture for any tests that need real files on disk.

```python
# tests/test_script.py
from pathlib import Path
from my_script import my_pure_function

def test_example(tmp_path: Path) -> None:
    f = tmp_path / "input.md"
    f.write_text("# Hello")
    result = my_pure_function(f)
    assert result == "expected"
```

If a script bundles all logic inside `main()`, refactor by extracting a pure function first. This keeps `main()` as a thin CLI wrapper and makes the logic independently testable.

### Running tests

The `.venv` must exist before running pytest. It is created the first time any script in the skill is executed:

```bash
# Create .venv (only needed once)
python3 scripts/script.py --help

# Run all tests (Linux/macOS)
scripts/.venv/bin/python -m pytest scripts/tests/ -v

# Run all tests (Windows)
scripts/.venv/Scripts/python -m pytest scripts/tests/ -v
```

### readme.md

A brief overview of these tests.

Example:

````markdown
# Tests

Unit tests for scripts.

## Usage

The `.venv` must exist before running tests. Run any script once to create it:

```bash
python3 scripts/script.py --help
```

```bash
# Linux/macOS
scripts/.venv/bin/python -m pytest scripts/tests/ -v

# Windows
scripts/.venv/Scripts/python -m pytest scripts/tests/ -v
```
````

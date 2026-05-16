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

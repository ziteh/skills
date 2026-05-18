# Tests

Unit tests for scripts.

## Usage

The `.venv` must exist before running pytest. It is created the first time any script in the skill is executed:

```bash
# Create .venv (only needed once)
python3 scripts/script.py --help

# Run all tests (Linux/macOS)
scripts/.venv/bin/python -m pytest scripts/tests/ -v

# Run all tests (Windows)
scripts/.venv/Scripts/python -m pytest scripts/tests/ -v
```

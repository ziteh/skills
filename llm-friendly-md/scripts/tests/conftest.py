"""
All scripts call `bootstrap.ensure()` at module level to set up the `.venv`.
`conftest.py` pre-populates `sys.modules["bootstrap"]` with a `MagicMock` so that
call becomes a no-op when scripts are imported during tests.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

# Prevent module-level bootstrap.ensure() from running when scripts are imported.
sys.modules["bootstrap"] = MagicMock()

# Make scripts importable by name.
sys.path.insert(0, str(Path(__file__).parent.parent))

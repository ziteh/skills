"""
Ensure the Python virtual environment is set up and dependencies are installed.

Usage:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill-maker" / "scripts"))
    import bootstrap  # pyright: ignore[reportMissingImports]
    bootstrap.ensure(Path(__file__).parent)  # pyright: ignore[reportUnknownMemberType]

    # ruff: noqa: E402
    import requests

Attributes:
    AUDIT_INTERVAL_SEC: Time interval in seconds to run pip-audit security checks.
    PIP_AUDIT_VER: The version of pip-audit to install.
"""

import sys
import shutil
import subprocess
import time
from pathlib import Path

AUDIT_INTERVAL_SEC = 60 * 60 * 24 * 7
PIP_AUDIT_VER = "==2.10.0"


class Colors:
    YELLOW = "\033[93m"
    GRAY = "\033[90m"
    ENDC = "\033[0m"


def _venv_python(venv: Path) -> Path:
    return (
        venv / "Scripts" / "python.exe"
        if sys.platform == "win32"
        else venv / "bin" / "python"
    )


def _venv_pip(venv: Path) -> Path:
    return (
        venv / "Scripts" / "pip.exe"
        if sys.platform == "win32"
        else venv / "bin" / "pip"
    )


def _venv_pip_audit(venv: Path) -> Path:
    return (
        venv / "Scripts" / "pip-audit.exe"
        if sys.platform == "win32"
        else venv / "bin" / "pip-audit"
    )


def _audit_timestamp_path(dir: Path) -> Path:
    return dir / ".audit_timestamp"


def _is_in_venv(venv: Path) -> bool:
    return Path(sys.prefix) == venv


def _create_venv(venv: Path) -> None:
    print(f"{Colors.GRAY}[bootstrap]{Colors.ENDC} Creating virtual environment: {venv}")
    if venv.exists():
        shutil.rmtree(venv)
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)


def _install_deps(venv: Path, requirements_txt: Path, pip_audit_ver: str) -> None:
    print(f"{Colors.GRAY}[bootstrap]{Colors.ENDC} Installing dependencies...")
    subprocess.run([str(_venv_pip(venv)), "install", "--upgrade", "pip"], check=True)
    if requirements_txt.exists():
        subprocess.run(
            [str(_venv_pip(venv)), "install", "-r", str(requirements_txt)], check=True
        )
    subprocess.run(
        [str(_venv_pip(venv)), "install", f"pip-audit{pip_audit_ver}"], check=True
    )


def _should_audit(venv: Path) -> bool:
    ts_file = _audit_timestamp_path(venv)
    if not ts_file.exists():
        return True
    try:
        last = float(ts_file.read_text().strip())
        return (time.time() - last) > AUDIT_INTERVAL_SEC
    except (ValueError, OSError):
        return True


def _run_audit(venv: Path) -> None:
    result = subprocess.run(
        [str(_venv_pip_audit(venv))], capture_output=True, text=True
    )
    _audit_timestamp_path(venv).write_text(str(time.time()))
    if result.returncode != 0:
        # Just print the warning and audit results, don't fail the whole process
        print(
            f"{Colors.YELLOW}[SECURITY WARNING]{Colors.ENDC} pip-audit found known vulnerabilities:"
        )
        print(result.stdout)
        print(
            "It is recommended to update the affected packages or verify if the vulnerabilities impact your use case."
        )


def ensure(script_dir: Path, pip_audit_ver: str = PIP_AUDIT_VER) -> None:
    """
    Ensure the virtual environment is set up and dependencies are installed.

    Args:
        script_dir: The directory containing the .py files (and optionally requirements.txt).
        pip_audit_ver: The version of pip-audit to install
    """
    venv = script_dir / ".venv"
    requirements_txt = script_dir / "requirements.txt"

    needs_install = not _venv_pip(venv).exists()
    if needs_install:
        _create_venv(venv)
        _install_deps(venv, requirements_txt, pip_audit_ver)

    if _should_audit(venv):
        _run_audit(venv)

    # If we're not already running inside the venv, re-run the script with the venv's Python
    if not _is_in_venv(venv):
        result = subprocess.run([str(_venv_python(venv))] + sys.argv)
        sys.exit(result.returncode)

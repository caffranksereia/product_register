import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

VENV_DIR = ROOT_DIR / ".venv"
ENV_FILE = ROOT_DIR / ".env"
REQUIREMENTS_FILE = ROOT_DIR / "requirements.txt"

VENV_PYTHON = (
    VENV_DIR / "Scripts" / "python.exe"
    if os.name == "nt"
    else VENV_DIR / "bin" / "python"
)


def create_venv() -> None:
    if not VENV_DIR.exists():
        print("Creating virtual environment...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
        )


def create_env() -> None:
    if not ENV_FILE.exists():
        print("Creating .env file...")

        ENV_FILE.write_text(
            "DB_HOST=localhost\n"
            "DB_PORT=5432\n"
            "DB_NAME=postgres\n"
            "DB_USER=postgres\n"
            "DB_PASSWORD=\n",
            encoding="utf-8",
        )


def install_dependencies() -> None:
    if not REQUIREMENTS_FILE.exists():
        raise FileNotFoundError("requirements.txt not found.")

    print("Installing dependencies...")

    subprocess.run(
        [
            str(VENV_PYTHON),
            "-m",
            "pip",
            "install",
            "-r",
            str(REQUIREMENTS_FILE),
        ],
        check=True,
    )


def setup_project() -> None:
    create_venv()
    create_env()
    install_dependencies()


def restart_in_venv() -> None:
    if sys.prefix != sys.base_prefix:
        return

    print("Restarting application inside virtual environment...")

    os.execv(
        str(VENV_PYTHON),
        [str(VENV_PYTHON), *sys.argv],
    )

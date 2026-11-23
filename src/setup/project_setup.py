import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

VENV_DIR = ROOT_DIR / ".venv"
ENV_FILE = ROOT_DIR / ".env"


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


def setup_project() -> None:
    create_venv()
    create_env()

# ==============================================================================
# SCRIPT: setup.py
# AUTHOR: Ed Johnson / Claude
# DATE:   2026-05-31
# VERSION: 1.0.0
# CONTEXT: AI_Transcriber — Portable Environment Bootstrap
# HARDWARE TARGET: Mac & Windows (External Drive / Cross-Platform)
#
# DESCRIPTION: Creates the platform-appropriate virtual environment (venv_mac or
#   venv_win) and installs dependencies from the matching requirements file.
#   Run once per machine, or re-run to reinstall after a drive-letter change.
#   Whisper.cpp must be built separately on Mac (see README).
# ==============================================================================

import sys
import os
import subprocess
import platform

IS_MAC     = platform.system() == "Darwin"
VENV_NAME  = "venv_mac" if IS_MAC else "venv_win"
REQS_FILE  = "requirements_mac.txt" if IS_MAC else "requirements_win.txt"

PIP = (
    os.path.join(VENV_NAME, "bin", "pip")
    if IS_MAC else
    os.path.join(VENV_NAME, "Scripts", "pip.exe")
)
ACTIVATE_HINT = (
    f"  source {VENV_NAME}/bin/activate"
    if IS_MAC else
    f"  {VENV_NAME}\\Scripts\\activate"
)


def run(cmd):
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    print(f"\nPlatform : {platform.system()}")
    print(f"Venv     : {VENV_NAME}")
    print(f"Reqs     : {REQS_FILE}\n")

    # Create venv if it doesn't exist
    if not os.path.exists(VENV_NAME):
        print(f"Creating virtual environment '{VENV_NAME}'...")
        run([sys.executable, "-m", "venv", VENV_NAME])
    else:
        print(f"Virtual environment '{VENV_NAME}' already exists — skipping creation.")

    # Upgrade pip
    print("\nUpgrading pip...")
    run([PIP, "install", "--upgrade", "pip"])

    # Install project requirements
    print(f"\nInstalling from {REQS_FILE}...")
    run([PIP, "install", "-r", REQS_FILE])

    print(f"\nDone. Activate the environment with:\n{ACTIVATE_HINT}\n")


if __name__ == "__main__":
    main()

#!/usr/bin/python3
import os, platform, pathlib
if platform.system() == "Windows":
    PYTHON = "python"
else:
    PYTHON = "python3"
VENV_DIR="./.venv"
REQUIREMENTS="./requirements.txt"
print("Setting up virtual environment...")
if not pathlib.Path(VENV_DIR).is_dir(): # Create venv if it doesn't exist
    os.system(PYTHON + " -m venv " + VENV_DIR)
    print("Created venv at " + VENV_DIR)
else:
    print("Using existing venv at " + VENV_DIR)
if pathlib.Path(REQUIREMENTS).is_file(): # Install dependencies if requirements file exists
    os.system(PYTHON + " -m pip install --upgrade pip --quiet")
    os.system(PYTHON + " -m pip install -r " + REQUIREMENTS)
    print("Installed dependencies from " + REQUIREMENTS)
else:
    print("No " + REQUIREMENTS + " found — skipping package install")
print()

print("Please run the command: \nsource " + VENV_DIR + "/bin/activate")
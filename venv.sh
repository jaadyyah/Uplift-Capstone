# /bin/bash
set -e 
PYTHON=${PYTHON:-python3}
VENV_DIR="./.venv"
REQUIREMENTS="./requirements.txt"
echo "Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then # Create venv if it doesn't exist
    $PYTHON -m venv "$VENV_DIR"
    echo "Created venv at $VENV_DIR"
else
    echo "Using existing venv at $VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install --upgrade pip --quiet
if [ -f "$REQUIREMENTS" ]; then # Install dependencies if requirements file exists
    pip install -r "$REQUIREMENTS"
    echo "Installed dependencies from $REQUIREMENTS"
else
    echo "No $REQUIREMENTS found — skipping package install"
fi

echo ""
echo "Done! Activate with: source $VENV_DIR/bin/activate"
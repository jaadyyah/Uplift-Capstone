# Stop on errors (like `set -e`)
$ErrorActionPreference = "Stop"

# Defaults
$PYTHON = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$VENV_DIR = ".\.venv"
$REQUIREMENTS = ".\requirements.txt"

Write-Host "Setting up virtual environment..."

if (-Not (Test-Path $VENV_DIR)) {
    # Create venv if it doesn't exist
    & $PYTHON -m venv $VENV_DIR
    Write-Host "Created venv at $VENV_DIR"
} else {
    Write-Host "Using existing venv at $VENV_DIR"
}

# Activate venv (PowerShell uses Activate.ps1)
$activateScript = Join-Path $VENV_DIR "Scripts\Activate.ps1"
. $activateScript

# Upgrade pip
pip install --upgrade pip --quiet

# Install dependencies if requirements file exists
if (Test-Path $REQUIREMENTS) {
    pip install -r $REQUIREMENTS
    Write-Host "Installed dependencies from $REQUIREMENTS"
} else {
    Write-Host "No $REQUIREMENTS found — skipping package install"
}

Write-Host ""
#!/bin/bash

echo "=========================================="
echo " 🐿️  Installing Rataitosk (macOS/Linux)"
echo "=========================================="

# 1. Check if Python is installed
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3.9+ is not installed."
  echo "💡 Please install it from https://www.python.org/downloads/"
  exit 1
fi

# 2. Check Python version (must be >= 3.9)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED="3.9"

vercomp () {
  [ "$1" = "$2" ] && return 0
  local IFS=.
  local i ver1=($1) ver2=($2)
  for ((i=0; i<${#ver1[@]}; i++)); do
    [[ -z ${ver2[i]} ]] && ver2[i]=0
    if ((10#${ver1[i]} < 10#${ver2[i]})); then return 1; fi
    if ((10#${ver1[i]} > 10#${ver2[i]})); then return 0; fi
  done
  return 0
}

vercomp $PYTHON_VERSION $REQUIRED
if [ $? -ne 0 ]; then
  echo "❌ Python version must be 3.9 or newer. Found: $PYTHON_VERSION"
  exit 1
fi

echo "✅ Python version $PYTHON_VERSION is OK."

# 3. Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv || {
  echo "❌ Failed to create virtual environment. Is venv module installed?"
  exit 1
}

# 4. Activate and install packages
echo "Activating environment and installing packages..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || {
  echo "❌ Dependency installation failed."
  exit 1
}

echo ""
echo "✅ Rataitosk is installed and ready."

echo ""
echo "➤ To run the tool:"
echo "   1. Place two PDFs in the input/ folder"
echo "   2. Run: python cli/run_rataitosk.py"
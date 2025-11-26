#!/bin/bash
# For macOS - opens the input folder for the user.

# --- Get the directory where this script is located ---
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$BASE_DIR"

echo "=========================================="
echo " 🐿️  Welcome to Rataitosk Document Analyzer"
echo "=========================================="
echo ""

# --- 1. Check for Python 3 ---
echo "💡 Step 1 of 5: Checking for Python..."
if ! command -v python3 &>/dev/null; then
  echo "❌ ERROR: Python 3 is not installed."
  echo "Please ask IT to install Python 3 from https://www.python.org/downloads/macos/"
  read -p "Press Enter to exit."
  exit 1
fi
echo "✅ Python found."
echo ""

# --- 2. Set up Virtual Environment ---
VENV_DIR="venv"
echo "💡 Step 2 of 5: Setting up environment..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR" || { echo "❌ ERROR: Failed to create environment."; read -p "Press Enter."; exit 1; }
fi
source "$VENV_DIR/bin/activate"
echo "✅ Environment ready."
echo ""

# --- 3. Install Dependencies ---
echo "💡 Step 3 of 5: Updating packages..."
pip install -r requirements.txt --quiet || { echo "❌ ERROR: Package installation failed."; read -p "Press Enter."; exit 1; }
echo "✅ Packages ready."
echo ""

# --- 4. Open Input Folder and Wait for User ---
echo "💡 Step 4 of 5: Add your files."
echo "The 'input' folder will now open."
open input

read -p "Please drag your two PDF files into the folder, then press Enter here to continue..."
echo ""


# --- 5. Run Analysis ---
echo "💡 Step 5 of 5: Analyzing documents..."
OUTPUT_HTML_PATH=$(python3 -m cli.run_rataitosk 2>/dev/null | grep "^OUTPUT_PATH:" | cut -d: -f2-)

if [ -z "$OUTPUT_HTML_PATH" ] || [[ ! "$OUTPUT_HTML_PATH" == *.html ]]; then
    echo "❌ Analysis failed. Please check messages above."
else
    echo "✅ Analysis complete! Opening your report..."
    open "$OUTPUT_HTML_PATH"
fi

echo ""
read -p "You can now close this window. Press Enter to exit."
deactivate
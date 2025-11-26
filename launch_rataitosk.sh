#!/bin/bash

echo "=========================================="
echo " 🐿️  Launching Rataitosk (Linux/macOS)"
echo "=========================================="

# 1. Check for venv
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found."
  echo "💡 Please run setup/install_rataitosk.sh first."
  exit 1
fi

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run the CLI script
echo "Running comparison..."
python cli/run_rataitosk.py

echo ""
echo "✅ Finished. Check the output/ folder."
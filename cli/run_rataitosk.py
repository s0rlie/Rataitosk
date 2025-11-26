# cli/run_rataitosk.py
"""
User-facing CLI entry point for Rataitosk.

Usage:
    python run_rataitosk.py --doc1 path/to/file1.pdf --doc2 path/to/file2.pdf

If no arguments are given, uses the first two PDFs found in /input.
"""

import argparse
import os
import glob
import json
import datetime
from typing import Optional, List
from config import settings
from core import engine, html_renderer

def find_input_pdfs() -> List[str]:
    """Find up to two PDF files in the input directory."""
    pdfs = glob.glob(os.path.join(settings.INPUT_DIR, "*.pdf"))
    return pdfs[:2] if len(pdfs) >= 2 else []

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Rataitosk document comparison")
    parser.add_argument("--doc1", type=str, help="Path to first PDF")
    parser.add_argument("--doc2", type=str, help="Path to second PDF")
    parser.add_argument("--output", choices=["html", "json", "both"], 
                       default=settings.DEFAULT_OUTPUT_FORMAT,
                       help="Output format (default: html)")
    return parser.parse_args()

def main():
    """Main entry point for CLI execution."""
    args = parse_args()
    
    doc1 = args.doc1
    doc2 = args.doc2
    
    if not doc1 or not doc2:
        print("[CLI] No input files provided. Trying to auto-detect two PDFs from /input...")
        docs = find_input_pdfs()
        if len(docs) < 2:
            print("❌ Could not find two PDFs in input/. Please use --doc1 and --doc2.")
            return
        doc1, doc2 = docs
        print(f"✓ Using: {doc1} and {doc2}")
    
    print("[CLI] Running Rataitosk engine...")
    results = engine.compare_documents(doc1, doc2)
    
    # Check for critical errors in results
    if results.get("axis_results") and len(results["axis_results"]) == 1:
        first_result = results["axis_results"][0]
        if first_result.get("axis") in ["ALL", "NONE"] and first_result.get("error"):
            print(f"❌ Analysis failed: {first_result['error']}")
            return
    
    html_path = None
    
    if args.output in ["html", "both"]:
        html_path = html_renderer.render_html(results)
        if html_path:
            print(f"✅ HTML saved to: {html_path}")
            # Output path for shell script integration
            print(f"OUTPUT_PATH:{html_path}")
        else:
            print("❌ HTML rendering failed.")
    
    if args.output in ["json", "both"]:
        if args.output == "json":
            # Generate path independently
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            json_path = os.path.join(settings.OUTPUT_DIR, f"results-{timestamp}.json")
        else:
            # Use HTML path if available
            if html_path is None:
                print("❌ Cannot generate JSON alongside HTML when HTML generation failed")
                return
            json_path = html_path.replace(".html", ".json")
        
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON saved to: {json_path}")
        except Exception as e:
            print(f"❌ Failed to save JSON: {e}")

if __name__ == "__main__":
    main()
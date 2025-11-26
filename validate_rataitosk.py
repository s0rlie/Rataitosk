# validate_rataitosk.py
"""
Sequential Rataitosk validator.

Runs core steps: PDF reading, chunking, embedding, scoring, and output.
Helps confirm the installation works and all modules are functional.
"""

import os
import time
from typing import Optional, Tuple, List, Dict, Any
from core import chunking, embedding, engine, html_renderer
from config import settings

EXAMPLE_PDF_1 = "input/NTNU-Strategi-2035.pdf"
EXAMPLE_PDF_2 = "input/NTNU-OK-Strategi-2035.pdf"

def step(name: str):
    """Print a section header for validation steps."""
    print(f"\n=== {name} ===")

def validate_files() -> bool:
    """Check if input PDF files exist."""
    step("Checking Input PDFs")
    for f in [EXAMPLE_PDF_1, EXAMPLE_PDF_2]:
        if not os.path.exists(f):
            print(f"❌ Missing: {f}")
            return False
    print("✅ Input PDFs found.")
    return True

def validate_chunking() -> Optional[Tuple[List[str], List[str]]]:
    """Test the chunking functionality."""
    step("Running Chunking")
    start = time.time()
    try:
        c1 = chunking.chunk_pdf(EXAMPLE_PDF_1)
        c2 = chunking.chunk_pdf(EXAMPLE_PDF_2)
        elapsed = time.time() - start
        print(f"✓ PDF 1: {len(c1)} chunks | PDF 2: {len(c2)} chunks")
        print(f"⏱ Chunking completed in {elapsed:.2f} seconds.")
        return c1, c2
    except Exception as e:
        print(f"❌ Chunking failed: {e}")
        return None

def validate_embedding():
    """Test the embedding model loading."""
    step("Loading Embedding Model")
    print("⏳ This may take 10–20 seconds on first run...")
    start = time.time()
    try:
        model = embedding.get_model()
        elapsed = time.time() - start
        print(f"✅ Model loaded: {type(model).__name__}")
        print(f"⏱ Load time: {elapsed:.2f} seconds.")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        raise

def validate_engine() -> Optional[Dict[str, Any]]:
    """Test the scoring engine."""
    step("Executing Scoring Engine")
    print("⚙️ Comparing documents and scoring axes...")
    start = time.time()
    try:
        results = engine.compare_documents(EXAMPLE_PDF_1, EXAMPLE_PDF_2)
        elapsed = time.time() - start
        
        # Extract axis results from new structure
        axis_results = results.get("axis_results", [])
        metadata = results.get("metadata", {})
        
        # Display results summary
        successful_axes = [r for r in axis_results if r.get("score") is not None]
        failed_axes = [r for r in axis_results if r.get("error")]
        
        print(f"✅ Scored {len(successful_axes)} axes successfully")
        if failed_axes:
            print(f"⚠️ {len(failed_axes)} axes failed")
        
        print(f"⏱ Processing time: {elapsed:.2f} seconds")
        
        # Display hardware info if available
        if metadata.get("hardware"):
            hw = metadata["hardware"]
            print(f"📊 System: {hw.get('platform', 'Unknown')}")
            print(f"   Python: {hw.get('python_version', 'Unknown')}")
            print(f"   CPU cores: {hw.get('cpu_cores', 'Unknown')}")
            print(f"   Memory: {hw.get('memory_gb', 'Unknown')} GB")
        
        return results
    except Exception as e:
        print(f"❌ Engine execution failed: {e}")
        return None

def validate_output(results: Dict[str, Any]):
    """Test HTML output generation."""
    step("Generating Output")
    try:
        out_path = html_renderer.render_html(results, "validation-output")
        if out_path:
            print(f"✅ HTML saved to: {out_path}")
        else:
            print("❌ Output rendering failed.")
    except Exception as e:
        print(f"❌ Output generation failed: {e}")

def run_all() -> bool:
    """Run all validation steps in sequence."""
    print("🔍 Starting Rataitosk system check...")
    print(f"📁 Working directory: {os.getcwd()}")
    
    if not validate_files():
        print("\n❌ Validation failed: Input files missing")
        print("💡 Please ensure example PDFs are in the input/ folder")
        return False
    
    try:
        # Test embedding model
        validate_embedding()
        
        # Test chunking
        result = validate_chunking()
        if not result:
            print("\n❌ Validation failed: Chunking error")
            return False
        
        # Test engine
        results = validate_engine()
        if not results:
            print("\n❌ Validation failed: Engine error")
            return False
        
        # Test output generation
        validate_output(results)
        
        print("\n" + "="*50)
        print("✅ All Rataitosk components validated successfully.")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"\n❌ Validation failed with error: {e}")
        print("💡 Check README.md for common issues")
        return False

if __name__ == "__main__":
    success = run_all()
    exit(0 if success else 1)
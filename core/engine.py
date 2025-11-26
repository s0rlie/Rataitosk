# core/engine.py
"""
Main scoring engine for Rataitosk.

Loads enabled axes from the registry and executes each one,
returning structured results for downstream output/logging.
"""
import os
import time
import importlib
import json
import platform
import psutil
from typing import Dict, List, Any, Optional
from config import settings
from core import chunking

def load_registry() -> List[Dict[str, Any]]:
    """
    Loads enabled axes from registry.json.
    
    Returns:
        List of axis metadata dicts with enabled axes only.
        
    Raises:
        FileNotFoundError: If registry.json is missing.
        json.JSONDecodeError: If registry.json is malformed.
    """
    try:
        with open(settings.AXIS_REGISTRY_PATH, "r", encoding="utf-8") as f:
            all_axes = json.load(f)
    except FileNotFoundError:
        print(f"❌ Registry file not found: {settings.AXIS_REGISTRY_PATH}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid registry JSON: {e}")
        return []
    
    return [axis for axis in all_axes if axis.get("enabled", False)]

def load_axis_module(axis_id: str):
    """
    Dynamically imports an axis scoring module.
    
    Args:
        axis_id: The identifier of the axis module to load.
        
    Returns:
        The imported module object.
        
    Raises:
        ImportError: If the module cannot be imported.
    """
    return importlib.import_module(f"axes.{axis_id}")

def get_hardware_info() -> Dict[str, Any]:
    """
    Get system hardware information for transparency and reproducibility.
    """
    try:
        import platform
        import psutil
        
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        memory_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        
        # Enhanced CPU model detection for Windows
        cpu_model = "Unknown CPU"
        try:
            if platform.system() == "Windows":
                import subprocess
                # Try wmic first
                try:
                    result = subprocess.run(
                        ["wmic", "cpu", "get", "name", "/value"], 
                        capture_output=True, 
                        text=True,
                        encoding='utf-8'
                    )
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if line.startswith('Name='):
                                cpu_model = line.split('=', 1)[1].strip()
                                break
                except:
                    # Fallback to platform.processor()
                    cpu_model = platform.processor()
                    if not cpu_model:
                        cpu_model = "Windows CPU"
            # ... rest of OS detection code
        except Exception as e:
            cpu_model = platform.machine() or "Unknown CPU"
        
        return {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_model": cpu_model,
            "cpu_cores": cpu_count_physical or 0,
            "cpu_threads": cpu_count_logical or 0,
            "memory_gb": memory_gb,
            "model_name": settings.EMBEDDING_MODEL_NAME
        }
    except Exception as e:
        return {
            "platform": "unknown",
            "python_version": "unknown", 
            "cpu_model": "Unknown CPU",
            "cpu_cores": 0,
            "cpu_threads": 0,
            "memory_gb": 0.0,
            "error": str(e)
        }

def compare_documents(doc1_path: str, doc2_path: str) -> Dict[str, Any]:
    """
    Compare two documents across all enabled scoring axes.
    
    Args:
        doc1_path: Path to first PDF.
        doc2_path: Path to second PDF.
        
    Returns:
        Dict with axis_results, metadata (hardware, timing), and document_info.
        Returns structured error on failure.
    """
    # Track processing time for performance transparency
    start_time = time.time()
    
    # Extract document names for display
    doc1_name = os.path.basename(doc1_path).replace('.pdf', '')
    doc2_name = os.path.basename(doc2_path).replace('.pdf', '')
    
    # Initialize result structure
    result_structure = {
        "axis_results": [],
        "metadata": {
            "hardware": get_hardware_info(),
            "processing_time_seconds": 0.0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "document_info": {
            "doc1_path": doc1_path,
            "doc2_path": doc2_path,
            "doc1_name": doc1_name,
            "doc2_name": doc2_name
        }
    }
    
    print(f"[Engine] Chunking documents...")
    
    # Perform chunking with error handling
    try:
        chunks1 = chunking.chunk_pdf(doc1_path)
        chunks2 = chunking.chunk_pdf(doc2_path)
    except Exception as e:
        print(f"❌ Chunking failed: {e}")
        result_structure["axis_results"].append({
            "axis": "ALL",
            "score": None,
            "doc1": doc1_name,
            "doc2": doc2_name,
            "error": f"Chunking failed: {str(e)}"
        })
        result_structure["metadata"]["processing_time_seconds"] = time.time() - start_time
        return result_structure
    
    # Validate chunks
    if not chunks1 or not chunks2:
        result_structure["axis_results"].append({
            "axis": "ALL",
            "score": None,
            "doc1": doc1_name,
            "doc2": doc2_name,
            "error": "One or both documents produced no valid chunks"
        })
        result_structure["metadata"]["processing_time_seconds"] = time.time() - start_time
        return result_structure
    
    # Store chunk counts for reference
    result_structure["document_info"]["chunks1_count"] = len(chunks1)
    result_structure["document_info"]["chunks2_count"] = len(chunks2)
    
    print("[Engine] Loading axis registry...")
    
    axes = load_registry()
    if not axes:
        print("⚠️ No axes enabled in registry")
        result_structure["axis_results"].append({
            "axis": "NONE",
            "score": None,
            "doc1": doc1_name,
            "doc2": doc2_name,
            "error": "No axes enabled in registry.json"
        })
        result_structure["metadata"]["processing_time_seconds"] = time.time() - start_time
        return result_structure
    
    # Process each axis
    for axis in axes:
        axis_id = axis["id"]
        print(f"[Engine] Scoring axis: {axis['label']} ({axis_id})")
        
        try:
            module = load_axis_module(axis_id)
            result = module.score(chunks1, chunks2, name1=doc1_name, name2=doc2_name)
            result["id"] = axis_id
            result["axis_name"] = axis["label"]
            result_structure["axis_results"].append(result)
        except Exception as e:
            print(f"❌ Axis '{axis_id}' failed: {e}")
            result_structure["axis_results"].append({
                "axis": axis["label"],
                "id": axis_id,
                "score": None,
                "doc1": doc1_name,
                "doc2": doc2_name,
                "error": str(e)
            })
    
    # Calculate final processing time
    result_structure["metadata"]["processing_time_seconds"] = round(time.time() - start_time, 2)
    
    print(f"[Engine] Processing completed in {result_structure['metadata']['processing_time_seconds']} seconds")
    
    return result_structure
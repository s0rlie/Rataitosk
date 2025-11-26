# core/html_renderer.py
"""
HTML renderer for Rataitosk output.

Uses Jinja2 templating to create a user-friendly report
from structured axis scores with full metadata.
"""

import os
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from config import settings


def render_html(results: Dict[str, Any], run_name: Optional[str] = None) -> Optional[str]:
    """
    Render an HTML file from the results and save it to the output directory.
    
    Args:
        results: Dictionary containing axis_results, metadata, and document_info
        run_name: Optional name prefix for the output file
        
    Returns:
        Path to the generated HTML file, or None if rendering fails
    """
    env = Environment(loader=FileSystemLoader("templates"))
    
    try:
        template = env.get_template("results.html")
    except TemplateNotFound:
        print("❌ Could not find results.html in templates/.")
        print("Please make sure templates/results.html exists and is readable.")
        return None
    
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    
    # Generate timestamp for filename (filesystem-safe)
    file_timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{run_name or 'results'}-{file_timestamp}.html"
    output_path = Path(settings.OUTPUT_DIR) / filename
    
    # Generate timestamp for display (human-readable)
    display_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract components from the structured results
    axis_results = results.get("axis_results", [])
    metadata = results.get("metadata", {})
    document_info = results.get("document_info", {})
    
    # Get hardware info with safe defaults
    hardware = metadata.get("hardware", {
        "platform": "Unknown",
        "python_version": "Unknown",
        "cpu_model": "Unknown CPU",
        "cpu_cores": 0,
        "cpu_threads": 0,
        "memory_gb": 0.0
    })
    
    # Get runtime with safe default
    runtime_seconds = metadata.get("processing_time_seconds", 0.0)
    
    # Get chunks processed (calculate if not provided)
    chunks_processed = metadata.get("chunks_processed")
    if chunks_processed is None:
        # Calculate from document_info if available
        doc1_chunks = document_info.get("doc1_chunks", 0)
        doc2_chunks = document_info.get("doc2_chunks", 0)
        chunks_processed = doc1_chunks + doc2_chunks
    
    # Pass structured data to template - let template handle formatting
    html = template.render(
        # Document metadata
        doc1_name=document_info.get("doc1_name", "Document 1"),
        doc2_name=document_info.get("doc2_name", "Document 2"),
        timestamp=display_timestamp,
        
        # Results
        results=axis_results,
        
        # Hardware and performance (structured data)
        hardware=hardware,  # Dictionary - template will format
        runtime=runtime_seconds,  # Float - template will format
        chunks_processed=doc1_chunks + doc2_chunks,
    )
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        print(f"❌ Failed to write HTML file: {e}")
        return None
    
    print(f"✅ HTML report saved to: {output_path}")
    
    # For macOS/Linux compatibility
    if hasattr(output_path, 'as_posix'):
        return output_path.as_posix()
    return str(output_path)

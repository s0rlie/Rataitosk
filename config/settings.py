# config/settings.py
"""
Configuration constants for Rataitosk.

Centralizes file paths, model selection, chunking behavior, and output settings.
"""

# -------- Model Settings --------
# HuggingFace model used for embedding
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Whether to show model download progress (set False for minimal CLI output)
SHOW_PROGRESS = True

# -------- File and Folder Paths --------
# Do not use absolute paths; these are relative to the project root
INPUT_DIR = "input"
OUTPUT_DIR = "output"
TEMPLATE_DIR = "templates"
LOG_DIR = "logs"
TEMP_DIR = "temp"

# -------- Output Settings --------
# Output format options: "html", "json", "both"
DEFAULT_OUTPUT_FORMAT = "html"

# Whether to include a visible Rataitosk footer in HTML output
INCLUDE_BRANDING = True

# Hidden reference tag for source tracking (in HTML source code)
HTML_SOURCE_TAG = '<meta name="generator" content="Rataitosk v1.0">'

# -------- Axis Registry File --------
AXIS_REGISTRY_PATH = "axes/registry.json"

# -------- Chunking Settings --------
# The chunking strategy determines the granularity of the analysis.
# Users can adjust CHUNK_SIZE to toggle between modes:
#
#   - Fine-grained Analysis (Recommended for detailed comparison):
#     Set CHUNK_SIZE = 2
#
#   - High-level Thematic Analysis (Recommended for executive summaries):
#     Set CHUNK_SIZE = 10
#
#   - Default (Balanced approach):
#     CHUNK_SIZE = 4

# Approximate number of sentences per chunk.
CHUNK_SIZE = 4

# Minimum characters allowed in a chunk (to avoid scoring empty fragments)
MIN_CHUNK_LENGTH = 100
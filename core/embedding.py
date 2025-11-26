# core/embedding.py
"""
Embedding module for Rataitosk.

Provides singleton SentenceTransformer instance supporting multilingual embeddings.
Axis-specific reference vectors are defined in individual axis modules.
"""

from sentence_transformers import SentenceTransformer
from config import settings

_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        print(f"[Embedding] Loading model: {settings.EMBEDDING_MODEL_NAME}")
        try:
            _model_instance = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
            _model_instance.eval()
        except Exception as e:
            if "connection" in str(e).lower():
                raise ConnectionError(
                    f"Failed to download model. Check internet connection.\n"
                    f"Model: {settings.EMBEDDING_MODEL_NAME}\n"
                    f"Error: {e}"
                )
            raise RuntimeError(f"Failed to load embedding model: {e}")
    return _model_instance
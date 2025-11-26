# axes/transformational_vision.py
"""
Transformational Vision axis for Rataitosk.

Measures relative emphasis on future-ambition and transformational language
across documents. Inspired by strategic intent theory (Hamel & Prahalad, 1994)
and transformational ambition research (Ahuja & Lampert, 2001), but uses a narrow
semantic proxy rather than assessing actual transformational capacity or change readiness.

Architecture: Single-Anchor Comparative Scoring
- Compares document similarity to transformational vision anchor
- Returns relative score indicating which document uses more transformational language

Method: Simple comparative scoring against single anchor:
    score = (doc1_similarity - doc2_similarity) * 100

The axis measures emphasis on future-ambitious language patterns, not actual
strategic capacity, innovation capability, or organizational readiness for change.

Reference: Table A1.2 in Appendix A
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.embedding import get_model
from config import settings

# Reference text from Table A1.2 (Appendix A)
# Adapted from Hamel & Prahalad (1994) and Ahuja & Lampert (2001)
# Represents future-ambitious transformational language
TRANSFORMATIONAL_VISION_ANCHOR = (
    "We aim to explore new directions that extend beyond our current capabilities. "
    "Emerging opportunities shape the areas we prepare to develop over time. "
    "Future priorities influence how we envision the organisation evolving. "
    "Our long-term direction points toward roles and outcomes that require growth beyond what we do today."
)

def score(doc1_chunks: list[str], doc2_chunks: list[str], *, name1="Document A", name2="Document B") -> dict:
    """
    Score Transformational Vision between documents.
    
    Returns relative score (-100 to +100) indicating which document places
    stronger emphasis on future ambitions beyond current capabilities.
    
    Positive score: Doc1 more transformational
    Negative score: Doc2 more transformational
    Near zero: Similar transformational emphasis
    """
    if not doc1_chunks or not doc2_chunks:
        return {
            "axis": "Transformational Vision",
            "score": None,
            "doc1": name1,
            "doc2": name2,
            "error": "One or both documents have no chunks."
        }

    model = get_model()

    # Encode transformational vision anchor
    anchor_vector = np.asarray(model.encode([TRANSFORMATIONAL_VISION_ANCHOR], show_progress_bar=False))[0]
    anchor_vector_2d = anchor_vector.reshape(1, -1)
    
    # Encode document chunks
    emb1 = np.asarray(model.encode(doc1_chunks, show_progress_bar=settings.SHOW_PROGRESS))
    emb2 = np.asarray(model.encode(doc2_chunks, show_progress_bar=settings.SHOW_PROGRESS))

    # Compare each document to anchor
    sim1 = cosine_similarity(emb1, anchor_vector_2d).mean()
    sim2 = cosine_similarity(emb2, anchor_vector_2d).mean()

    # Relative comparison: positive if doc1 more transformational, negative if doc2 more transformational
    relative_score = (sim1 - sim2) * 100

    return {
        "axis": "Transformational Vision",
        "score": round(relative_score, 2),
        "doc1": name1,
        "doc2": name2,
        "anchor": "Future ambitions beyond current capabilities",
        "method": "single_anchor_comparative",
        "chunks1": len(doc1_chunks),
        "chunks2": len(doc2_chunks),
        "interpretation": (
            "Positive: Doc1 more transformational language. "
            "Negative: Doc2 more transformational language. "
            "Near zero: Similar transformational emphasis. "
            "Measures language patterns, not strategic capacity."
        )
    }
# axes/operational_grounding.py
"""
Operational Grounding axis for Rataitosk.

Measures relative emphasis on present-capability and operational-feasibility
language across documents. Inspired by exploitation logic (March, 1991) and
strategic fit theory (Henderson & Venkatraman, 1993), but uses a narrow semantic
proxy rather than assessing actual organizational capacity or feasibility.

Architecture: Single-Anchor Comparative Scoring
- Compares document similarity to operational grounding anchor
- Returns relative score indicating which document uses more operationally-grounded language

Method: Simple comparative scoring against single anchor:
    score = (doc1_similarity - doc2_similarity) * 100

The axis measures emphasis on present-capability language patterns, not actual
operational feasibility, strategic alignment, or implementation readiness.

Reference: Table A1.2 in Appendix A
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.embedding import get_model
from config import settings

OPERATIONAL_GROUNDING_ANCHOR = (
    "Our current capabilities and ongoing activities form the basis for the priorities we put forward. "
    "Existing processes, resources, and areas of expertise support the work already in progress. "
    "We focus on actions that can be implemented within today's structures. "
    "Our direction builds on what the organisation can deliver in practice at present."
)

def score(doc1_chunks: list[str], doc2_chunks: list[str], *, name1="Document A", name2="Document B") -> dict:
    """
    Score Operational Grounding between documents.
    
    Returns relative score (-100 to +100) indicating which document places
    stronger emphasis on current capabilities and operational feasibility language.
    
    Positive score: Doc1 more operationally grounded
    Negative score: Doc2 more operationally grounded
    Near zero: Similar operational emphasis
    """
    if not doc1_chunks or not doc2_chunks:
        return {
            "axis": "Operational Grounding",
            "score": None,
            "doc1": name1,
            "doc2": name2,
            "error": "One or both documents have no chunks."
        }

    model = get_model()

    # Encode operational grounding anchor
    anchor_vector = np.asarray(model.encode([OPERATIONAL_GROUNDING_ANCHOR], show_progress_bar=False))[0]
    anchor_vector_2d = anchor_vector.reshape(1, -1)
    
    # Encode document chunks
    emb1 = np.asarray(model.encode(doc1_chunks, show_progress_bar=settings.SHOW_PROGRESS))
    emb2 = np.asarray(model.encode(doc2_chunks, show_progress_bar=settings.SHOW_PROGRESS))

    # Compare each document to anchor
    sim1 = cosine_similarity(emb1, anchor_vector_2d).mean()
    sim2 = cosine_similarity(emb2, anchor_vector_2d).mean()

    # Relative comparison: positive if doc1 more grounded, negative if doc2 more grounded
    relative_score = (sim1 - sim2) * 100

    return {
        "axis": "Operational Grounding",
        "score": round(relative_score, 2),
        "doc1": name1,
        "doc2": name2,
        "anchor": "Present capabilities and operational feasibility",
        "method": "single_anchor_comparative",
        "chunks1": len(doc1_chunks),
        "chunks2": len(doc2_chunks),
        "interpretation": (
            "Positive: Doc1 more operationally grounded language. "
            "Negative: Doc2 more operationally grounded language. "
            "Near zero: Similar operational emphasis. "
            "Measures language patterns, not actual feasibility."
        )
    }
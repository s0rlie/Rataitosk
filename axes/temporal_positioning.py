# axes/temporal_positioning.py
"""
Temporal Positioning axis for Rataitosk.

Measures relative emphasis on present-focused versus future-focused language
across documents. Inspired by Temporal Work Theory (Kaplan & Orlikowski, 2013)
but uses a narrow semantic proxy rather than modeling interpretive processes.

Architecture: Differential Two-Anchor Scoring
- Compares document similarity to two oppositional anchors (present vs future)
- Returns relative score indicating directional temporal emphasis

Method: For each document, computes differential similarity:
    temporal_emphasis = similarity_to_future - similarity_to_present
Then compares:
    relative_score = (doc1_emphasis - doc2_emphasis) * 100

The axis highlights differences in temporal emphasis without interpreting
intent, narrative coherence, or strategic feasibility.

Reference: Table A1.2 in Appendix A
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.embedding import get_model
from config import settings



# Reference text adapted for present-oriented temporal emphasis
# Focused on current capabilities, ongoing work, and immediate priorities
PRESENT_ANCHOR = (
    "Our current capabilities and ongoing work guide the priorities we address now. "
    "Existing processes and established practices form the basis for actions underway. "
    "We focus on what the organisation delivers today and the tasks in progress. "
    "Present commitments shape the immediate steps we take."
)

# Reference text adapted for future-oriented temporal emphasis
# Focused on emerging possibilities, upcoming developments, and long-term evolution
FUTURE_ANCHOR = (
    "We prepare for emerging possibilities that extend beyond current activity. "
    "Upcoming developments shape the direction we envision over time. "
    "Future goals influence how we anticipate the organisation evolving. "
    "Long-term priorities point toward capabilities we aim to develop."
)

def score(doc1_chunks: list[str], doc2_chunks: list[str], *, name1="Document A", name2="Document B") -> dict:
    """
    Score Temporal Positioning between documents.
    
    Returns relative score (-100 to +100) indicating which document uses
    more future-focused language relative to present-focused language.
    
    Positive score: Doc1 more future-oriented
    Negative score: Doc2 more future-oriented
    Near zero: Similar temporal emphasis
    """
    if not doc1_chunks or not doc2_chunks:
        return {
            "axis": "Temporal Positioning",
            "score": None,
            "doc1": name1,
            "doc2": name2,
            "error": "One or both documents have no chunks."
        }

    model = get_model()

    # Encode both anchors
    present_vec = np.asarray(model.encode([PRESENT_ANCHOR], show_progress_bar=False))[0]
    future_vec = np.asarray(model.encode([FUTURE_ANCHOR], show_progress_bar=False))[0]
    
    # Reshape for cosine_similarity (needs 2D)
    present_vec_2d = present_vec.reshape(1, -1)
    future_vec_2d = future_vec.reshape(1, -1)
    
    # Encode document chunks
    emb1 = np.asarray(model.encode(doc1_chunks, show_progress_bar=settings.SHOW_PROGRESS))
    emb2 = np.asarray(model.encode(doc2_chunks, show_progress_bar=settings.SHOW_PROGRESS))

    # Calculate temporal emphasis for each document (future - present)
    doc1_to_present = cosine_similarity(emb1, present_vec_2d).mean()
    doc1_to_future = cosine_similarity(emb1, future_vec_2d).mean()
    doc1_emphasis = doc1_to_future - doc1_to_present
    
    doc2_to_present = cosine_similarity(emb2, present_vec_2d).mean()
    doc2_to_future = cosine_similarity(emb2, future_vec_2d).mean()
    doc2_emphasis = doc2_to_future - doc2_to_present
    
    # Relative comparison between documents
    relative_score = (doc1_emphasis - doc2_emphasis) * 100

    return {
        "axis": "Temporal Positioning",
        "score": round(relative_score, 2),
        "doc1": name1,
        "doc2": name2,
        "anchors": "Present-focused vs Future-focused language",
        "method": "differential_two_anchor",
        "chunks1": len(doc1_chunks),
        "chunks2": len(doc2_chunks),
        "interpretation": (
            "Positive: Doc1 more future-focused. "
            "Negative: Doc2 more future-focused. "
            "Near zero: Similar temporal emphasis. "
            "Measures language patterns, not strategic intent."
        )
    }
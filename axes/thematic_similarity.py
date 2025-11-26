# axes/thematic_similarity.py
"""
Thematic Similarity axis.

Measures baseline semantic similarity between documents using mean pairwise
chunk-chunk cosine similarity without concept anchoring.

Theoretical Foundation:
- Distributional semantics (Harris, 1954)
- Semantic similarity theory (Reimers & Gurevych, 2019)

Reference: Table A1.2 in Appendix A
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from core.embedding import get_model
from config import settings

def score(doc1_chunks: list[str], doc2_chunks: list[str], *, name1="Document A", name2="Document B") -> dict:
    if not doc1_chunks or not doc2_chunks:
        return {
            "axis": "Thematic Similarity",
            "score": None,
            "doc1": name1,
            "doc2": name2,
            "error": "One or both documents have no chunks."
        }

    model = get_model()
    all_chunks = doc1_chunks + doc2_chunks

    # Ensure embeddings are NumPy arrays
    embeddings = np.asarray(model.encode(all_chunks, show_progress_bar=settings.SHOW_PROGRESS))
    emb1 = embeddings[:len(doc1_chunks)]
    emb2 = embeddings[len(doc1_chunks):]

    sim_matrix = cosine_similarity(emb1, emb2)
    avg_score = np.mean(sim_matrix) * 100

    # Prepare chunk pairs
    pairs = []
    for i, chunk1 in enumerate(doc1_chunks):
        for j, chunk2 in enumerate(doc2_chunks):
            score = sim_matrix[i, j]
            pairs.append((chunk1, chunk2, float(score)))

    # Sort by similarity
    pairs.sort(key=lambda x: x[2])
    bottom5 = pairs[:10]
    top5 = pairs[-10:]

    return {
        "axis": "Thematic Similarity",
        "score": round(avg_score, 2),
        "doc1": name1,
        "doc2": name2,
        "method": "cosine_similarity",
        "chunks1": len(doc1_chunks),
        "chunks2": len(doc2_chunks),
        "top_chunks": top5,
        "bottom_chunks": bottom5
    }

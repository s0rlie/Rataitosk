# core/chunking.py
"""
Chunking logic for Rataitosk.

Extracts text from PDFs and splits them into fixed-size sentence-based chunks.

Designed to:
- Work on plain PDFs (non-scanned)
- Produce overlapping or non-overlapping semantic windows
- Minimize dependency overhead
"""

import fitz  # PyMuPDF
import nltk
import re
from config import settings

# Ensure the correct tokenizer is available (auto-downloads if needed)
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    print("NLTK 'punkt_tab' not found. Downloading...")
    nltk.download("punkt_tab")

from nltk.tokenize import sent_tokenize


def extract_text_from_pdf(path: str) -> str:
    """
    Extracts and concatenates text from a PDF file, cleaning up excessive whitespace
    and non-printable characters.
    """
    with fitz.open(path) as doc:
        raw_text = "\n".join(page.get_text() for page in doc) # type: ignore[attr-defined]
 
    # 1. Replace 3 or more consecutive newlines with just two.
    cleaned_text = re.sub(r'\n{3,}', '\n\n', raw_text)
 
    # 2. Replace 2 or more consecutive spaces with a single space.
    cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)

    # 3. Replace the 'form feed' character with a space.
    cleaned_text = cleaned_text.replace('\f', ' ')
 
    # 4. Remove other non-printable control characters.
    # This regex targets characters in the C0 and C1 control blocks.
    cleaned_text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', cleaned_text)
 
    return cleaned_text

def chunk_text(text, chunk_size=settings.CHUNK_SIZE):
    """
    Splits text into sentence-based chunks.

    Each chunk contains approximately `chunk_size` sentences.
    Returns a list of strings (chunks).
    """
    sentences = sent_tokenize(text)
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        # 1. Get the sentences for the current chunk.
        current_sentences = sentences[i:i + chunk_size]
        
        # 2. Filter out any "sentences" that are empty or just whitespace.
        non_empty_sentences = [s for s in current_sentences if s.strip()]
        
        # 3. If there are no valid sentences left, skip to the next iteration.
        if not non_empty_sentences:
            continue

        # 4. Join only the non-empty sentences.
        chunk = " ".join(non_empty_sentences).strip()

        if len(chunk) >= settings.MIN_CHUNK_LENGTH:
            chunks.append(chunk)

    return chunks

def chunk_pdf(path):
    """
    Full pipeline: PDF → text → chunks
    Returns a list of chunk strings.
    """
    text = extract_text_from_pdf(path)
    return chunk_text(text)
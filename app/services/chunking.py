import re
from typing import List


def fixed_chunk(text: str, size: int = 400, overlap: int = 40) -> List[str]:
    if size <= 0:
        raise ValueError(f"Chunk size must be positive, got {size}")
    if overlap < 0:
        raise ValueError(f"Overlap must be non-negative, got {overlap}")
    if overlap >= size:
        raise ValueError(f"Overlap ({overlap}) must be less than chunk size ({size})")
    
    if not text:
        return []
    
    chunks: List[str] = []
    start = 0
    
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    
    return chunks


def sentence_chunk(text: str, max_sentences: int = 5) -> List[str]:
    if max_sentences < 1:
        raise ValueError(f"max_sentences must be at least 1, got {max_sentences}")
    
    if not text:
        return []
    
    # Split on sentence boundaries (., !, ?) followed by whitespace
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out empty sentences
    sentences = [s for s in sentences if s.strip()]
    
    return [
        " ".join(sentences[i:i + max_sentences])
        for i in range(0, len(sentences), max_sentences)
    ]
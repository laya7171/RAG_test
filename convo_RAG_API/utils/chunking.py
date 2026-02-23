"""
Text chunking strategies.
Supports fixed-length and sentence-based chunking.
"""
import re
from typing import List
from config import settings


def fixed_length_chunking(
    text: str,
    chunk_size: int = None,
    overlap: int = None
) -> List[str]:
    """
    Split text into fixed-length chunks with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk (default from settings)
        overlap: Overlap between chunks (default from settings)
        
    Returns:
        List of text chunks
    """
    chunk_size = chunk_size or settings.FIXED_CHUNK_SIZE
    overlap = overlap or settings.FIXED_CHUNK_OVERLAP
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def sentence_chunking(
    text: str,
    max_chunk_size: int = None
) -> List[str]:
    """
    Split text into chunks based on sentences.
    
    Args:
        text: Text to chunk
        max_chunk_size: Maximum sentences per chunk (default from settings)
        
    Returns:
        List of text chunks
    """
    max_chunk_size = max_chunk_size or settings.SENTENCE_MAX_CHUNK_SIZE
    
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    
    for i in range(0, len(sentences), max_chunk_size):
        chunk = " ".join(sentences[i: i + max_chunk_size])
        chunks.append(chunk)
    
    return chunks


def chunk_text(text: str, strategy: str) -> List[str]:
    """
    Chunk text using the specified strategy.
    
    Args:
        text: Text to chunk
        strategy: Chunking strategy ('fixed' or 'sentence')
        
    Returns:
        List of text chunks
        
    Raises:
        ValueError: If strategy is not supported
    """
    if strategy == "fixed":
        return fixed_length_chunking(text)
    elif strategy == "sentence":
        return sentence_chunking(text)
    else:
        raise ValueError(f"Unsupported chunking strategy: {strategy}")

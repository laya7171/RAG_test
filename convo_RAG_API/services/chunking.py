import re
from typing import List

def fixed_chunk(text: str, size: int = 400, overlap: int = 40)-> List[str]:

    chunks = []
    start = 0
    while start <len(text):
        end = start + size 
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def sentence_chunk(text: str, max_sentences: int = 5) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [
        " ".join(sentences[i:i + max_sentences])
        for i in range(0, len(sentences), max_sentences)
    ]
from typing import List, Dict, Any
from pinecone import Pinecone
from core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

def get_index():
    """Lazy load the index to avoid errors at import time."""
    return pc.Index(settings.PINECONE_INDEX)

def upsert_vectors(vector_id: str, embedding: List[float], metadata: Dict[str, Any]) -> None:
    """Upsert a single vector to Pinecone index."""
    index = get_index()
    index.upsert([(vector_id, embedding, metadata)])

def query_vectors(query_embedding: List[float], top_k: int = 5) -> Dict[str, Any]:
    """Query vectors from Pinecone index."""
    index = get_index()
    return index.query(query_embedding, top_k=top_k, include_metadata=True)
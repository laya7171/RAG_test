from typing import List, Dict, Any, Optional
from pinecone import Pinecone, PineconeException
from core.config import settings

# Initialize Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)


def get_index():
    try:
        return pc.Index(settings.PINECONE_INDEX)
    except Exception as e:
        raise PineconeException(f"Failed to access Pinecone index '{settings.PINECONE_INDEX}': {str(e)}") from e


def upsert_vectors(
    vector_id: str,
    embedding: List[float],
    metadata: Dict[str, Any],
    namespace: Optional[str] = None
) -> None:
    if not vector_id:
        raise ValueError("vector_id cannot be empty")
    if not embedding or not isinstance(embedding, list):
        raise ValueError("embedding must be a non-empty list of floats")
    if not metadata:
        raise ValueError("metadata cannot be empty")
    
    try:
        index = get_index()
        index.upsert(
            vectors=[(vector_id, embedding, metadata)],
            namespace=namespace
        )
    except Exception as e:
        raise PineconeException(f"Failed to upsert vector '{vector_id}': {str(e)}") from e


def query_vectors(
    query_embedding: List[float],
    top_k: int = 5,
    namespace: Optional[str] = None,
    filter_dict: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if not query_embedding or not isinstance(query_embedding, list):
        raise ValueError("query_embedding must be a non-empty list of floats")
    if top_k < 1:
        raise ValueError(f"top_k must be at least 1, got {top_k}")
    
    try:
        index = get_index()
        return index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace,
            filter=filter_dict
        )
    except Exception as e:
        raise PineconeException(f"Failed to query vectors: {str(e)}") from e
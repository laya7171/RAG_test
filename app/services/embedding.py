from typing import List
from openai import OpenAI, OpenAIError
from core.config import settings

# Initialize OpenAI client with API key from settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def embed_text(text: str, model: str = "text-embedding-3-small") -> List[float]:
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    try:
        response = client.embeddings.create(
            model=model,
            input=text.strip()
        )
        return response.data[0].embedding
    
    except OpenAIError as e:
        raise OpenAIError(f"Failed to generate embedding: {str(e)}") from e


def embed_texts_batch(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    if not texts:
        raise ValueError("Input texts list cannot be empty")
    
    # Filter and strip texts, validate they're not empty
    processed_texts = [t.strip() for t in texts if t and t.strip()]
    if len(processed_texts) != len(texts):
        raise ValueError("All input texts must be non-empty")
    
    try:
        response = client.embeddings.create(
            model=model,
            input=processed_texts
        )
        return [item.embedding for item in response.data]
    
    except OpenAIError as e:
        raise OpenAIError(f"Failed to generate embeddings batch: {str(e)}") from e
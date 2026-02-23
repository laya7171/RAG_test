from typing import List
from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def embed_text(text: str) -> List[float]:
    """Generate embedding for a single text using OpenAI."""
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding
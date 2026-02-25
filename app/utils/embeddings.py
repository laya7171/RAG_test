from openai import OpenAI
from typing import List
from config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_embeddings(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        input=texts,
        model=settings.EMBEDDING_MODEL
    )
    
    return [item.embedding for item in response.data]
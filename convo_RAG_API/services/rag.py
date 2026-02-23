from langchain_ollama import OllamaLLM
from services.vector_store import query_vectors
from services.embedding import embed_text

llm = OllamaLLM(model="llama3.2")

def generate_answer(query: str):
    query_embedding = embed_text(query)
    results = query_vectors(query_embedding)

    context = "\n\n".join([res['metadata']['text'] for res in results])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    response = llm.invoke(prompt)
    return response
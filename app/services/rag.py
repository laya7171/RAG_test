from typing import List, Dict, Any, Optional
from services.vector_store import query_vectors
from services.embedding import embed_text
from services.llm_service import generate_chat_response


def generate_answer(
    query: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    top_k: int = 5,
    use_openai: bool = False
) -> str:
    try:
        # Step 1: Generate embedding for the query
        query_embedding = embed_text(query)
        
        # Step 2: Search for relevant documents
        search_results = query_vectors(query_embedding, top_k=top_k)
        
        # Step 3: Build context from retrieved documents
        context_chunks = []
        if 'matches' in search_results:
            for match in search_results['matches']:
                if 'metadata' in match and 'text' in match['metadata']:
                    context_chunks.append(match['metadata']['text'])
        
        # Join context chunks
        context = "\n\n".join(context_chunks) if context_chunks else "No relevant context found."
        
        # Step 4: Generate response using LLM
        response = generate_chat_response(
            query=query,
            context=context,
            conversation_history=conversation_history,
            use_openai=use_openai
        )
        
        return response
    
    except Exception as e:
        print(f"Error in RAG pipeline: {e}")
        return f"I apologize, but I encountered an error processing your query. Please try again."
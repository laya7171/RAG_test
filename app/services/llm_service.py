import json
import re
from typing import Optional, Dict, Any, List
from langchain_ollama import OllamaLLM
from openai import OpenAI
from core.config import settings

# Initialize LLM clients
ollama_llm = OllamaLLM(model="llama3.2")
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


def generate_chat_response(
    query: str,
    context: str,
    conversation_history: List[Dict[str, str]] = None,
    use_openai: bool = False
) -> str:
    # Build conversation history text
    history_text = ""
    if conversation_history:
        history_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in conversation_history[-5:]  # Last 5 messages
        ])
    
    # Build prompt
    history_section = f"Conversation History:\n{history_text}\n" if history_text else ""
    prompt = f"""You are a helpful AI assistant. Use the provided context to answer the user's question.
If the user is trying to book an interview, collect their name, email, date, and time.

{history_section}Context from documents:
{context}

Current Question: {query}

Answer (be helpful and conversational):"""
    
    if use_openai and openai_client:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    else:
        return ollama_llm.invoke(prompt)


def extract_booking_info(conversation_history: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    if not conversation_history:
        return None
    
    # Build conversation text
    conversation_text = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in conversation_history
    ])
    
    # Prompt for extraction
    extraction_prompt = f"""Analyze this conversation and extract interview booking information.
Return ONLY a JSON object with these fields if all are present: name, email, date, time.
If any information is missing, return an empty JSON object {{}}.

Conversation:
{conversation_text}

Extracted booking info (JSON only):"""
    
    try:
        response = ollama_llm.invoke(extraction_prompt)
        
        # Try to extract JSON from response
        json_match = re.search(r'\{[^{}]*\}', response)
        if json_match:
            booking_data = json.loads(json_match.group())
            
            # Validate all required fields are present
            required_fields = ['name', 'email', 'date', 'time']
            if all(field in booking_data and booking_data[field] for field in required_fields):
                return booking_data
        
        return None
    
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error extracting booking info: {e}")
        return None


def detect_booking_intent(query: str) -> bool:
    booking_keywords = [
        'book', 'schedule', 'appointment', 'interview',
        'meeting', 'reserve', 'set up', 'arrange'
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in booking_keywords)


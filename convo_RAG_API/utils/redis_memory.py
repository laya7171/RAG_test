"""
Redis-based conversation history management.
Stores and retrieves chat history for sessions.
"""
import json
from typing import List
import redis
from config import settings


_redis = redis.from_url(settings.REDIS_URL, decode_responses=True)


def _session_key(session_id: str) -> str:
    """Generate Redis key for a session."""
    return f"chat_history:{session_id}"


def get_history(session_id: str) -> List[dict]:
    """
    Retrieve full conversation history for a session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        List of message dictionaries with 'role' and 'content'
    """
    raw = _redis.get(_session_key(session_id))
    if not raw:
        return []
    return json.loads(raw)


def append_message(session_id: str, role: str, content: str) -> None:
    """
    Append a message to session history and reset TTL.
    
    Args:
        session_id: Unique session identifier
        role: Message role ('user' or 'assistant')
        content: Message content
    """
    history = get_history(session_id)
    history.append({"role": role, "content": content})
    _redis.set(
        _session_key(session_id),
        json.dumps(history),
        ex=settings.CHAT_HISTORY_TTL
    )


def clear_history(session_id: str) -> None:
    """
    Clear conversation history for a session.
    
    Args:
        session_id: Unique session identifier
    """
    _redis.delete(_session_key(session_id))
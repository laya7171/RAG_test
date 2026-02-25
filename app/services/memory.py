import json
from typing import List, Dict, Any
import redis
from core.config import settings

# Initialize Redis connection
_redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


def _session_key(session_id: str) -> str:
    return f"chat_history:{session_id}"


def get_history(session_id: str) -> List[Dict[str, str]]:
    try:
        raw = _redis_client.get(_session_key(session_id))
        if not raw:
            return []
        return json.loads(raw)
    except (redis.RedisError, json.JSONDecodeError) as e:
        print(f"Error retrieving history for session {session_id}: {e}")
        return []


def save_history(session_id: str, history: List[Dict[str, str]]) -> None:
    try:
        _redis_client.set(
            _session_key(session_id),
            json.dumps(history),
            ex=86400  # 24 hour TTL
        )
    except (redis.RedisError, TypeError, ValueError) as e:
        print(f"Error saving history for session {session_id}: {e}")


def append_message(session_id: str, role: str, content: str) -> None:
    history = get_history(session_id)
    history.append({"role": role, "content": content})
    save_history(session_id, history)


def clear_history(session_id: str) -> None:
    try:
        _redis_client.delete(_session_key(session_id))
    except redis.RedisError as e:
        print(f"Error clearing history for session {session_id}: {e}")
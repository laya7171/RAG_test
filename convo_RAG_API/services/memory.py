# In-memory storage for chat history (replace with Redis in production)
_memory_store = {}

def get_history(session_id: str):
    return _memory_store.get(session_id, [])

def save_history(session_id: str, history):
    _memory_store[session_id] = history
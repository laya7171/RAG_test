from fastapi import APIRouter
from schemas.chat import ChatRequest
from services.rag import generate_answer
from services.memory import get_history, save_history

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest):
    history = get_history(request.session_id)

    answer = generate_answer(request.query)

    history.append({"user": request.query, "assistant": answer})
    save_history(request.session_id, history)

    return {"answer": answer}
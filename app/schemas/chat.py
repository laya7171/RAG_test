from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from schemas.booking import BookingResponse


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique session identifier for conversation tracking",
        min_length=1
    )
    query: str = Field(
        ...,
        description="User's question or message",
        min_length=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "user123_session456",
                "query": "What is the main topic of the uploaded document?"
            }
        }


class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Generated answer from the conversational RAG system"
    )
    booking: Optional[BookingResponse] = Field(
        None,
        description="Booking information if an interview was successfully booked"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "The main topic of the document is machine learning and its applications in healthcare.",
                "booking": None
            }
        }
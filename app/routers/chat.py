"""Chat API router for conversational RAG.

This module provides the REST API endpoint for chat interactions,
including multi-turn conversations and interview booking support.
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse
from services.rag import generate_answer
from services.memory import get_history, append_message, clear_history
from services.llm_service import extract_booking_info, detect_booking_intent
from services.booking import save_booking
from db.session import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """Process a chat message with RAG and booking support.
    
    This endpoint:
    1. Retrieves conversation history from Redis
    2. Generates answer using RAG with multi-turn context
    3. Detects and extracts booking information if present
    4. Saves booking to database if complete
    5. Updates conversation history in Redis
    
    Args:
        request: Chat request containing session_id and query.
        db: Database session (injected by FastAPI).
    
    Returns:
        ChatResponse with generated answer and optional booking confirmation.
    
    Raises:
        HTTPException 400: If request validation fails.
        HTTPException 500: If processing fails.
    """
    try:
        # Validate request
        if not request.session_id or not request.query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="session_id and query are required"
            )
        
        # Retrieve conversation history
        history = get_history(request.session_id)
        
        # Add user message to history
        append_message(request.session_id, "user", request.query)
        
        # Generate answer using RAG with conversation context
        answer = generate_answer(
            query=request.query,
            conversation_history=history,
            top_k=5,
            use_openai=False
        )
        
        # Add assistant response to history
        append_message(request.session_id, "assistant", answer)
        
        # Check for booking intent and extract information
        booking_response = None
        if detect_booking_intent(request.query):
            # Get updated history including current exchange
            updated_history = get_history(request.session_id)
            booking_info = extract_booking_info(updated_history)
            
            # If booking info is complete, save to database
            if booking_info:
                try:
                    saved_booking = save_booking(db, booking_info)
                    logger.info(f"Booking saved: {saved_booking.id}")
                    
                    # Add confirmation to response
                    answer += f"\n\n✓ Interview booked successfully! Booking ID: {saved_booking.id}"
                    
                    # Return structured booking data
                    booking_response = {
                        "id": str(saved_booking.id),
                        "name": saved_booking.name,
                        "email": saved_booking.email,
                        "date": saved_booking.date,
                        "time": saved_booking.time,
                        "message": "Interview booked successfully"
                    }
                
                except Exception as e:
                    logger.error(f"Error saving booking: {e}")
                    answer += "\n\nNote: There was an issue saving your booking. Please try again."
        
        return ChatResponse(answer=answer, booking=booking_response)
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )


@router.delete("/history/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_chat_history(session_id: str) -> None:
    """Clear conversation history for a session.
    
    Args:
        session_id: Session identifier to clear history for.
    """
    try:
        clear_history(session_id)
    except Exception as e:
        logger.error(f"Error clearing history for session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear chat history"
        )


@router.get("/history/{session_id}", status_code=status.HTTP_200_OK)
def get_chat_history(session_id: str) -> Dict[str, Any]:
    """Retrieve conversation history for a session.
    
    Args:
        session_id: Session identifier to retrieve history for.
    
    Returns:
        Dictionary with session_id and history list.
    """
    try:
        history = get_history(session_id)
        return {
            "session_id": session_id,
            "history": history,
            "message_count": len(history)
        }
    except Exception as e:
        logger.error(f"Error retrieving history for session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history"
        )
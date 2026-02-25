from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import Booking


def save_booking(db: Session, data: Dict[str, str]) -> Booking:
    # Validate required fields
    required_fields = ['name', 'email', 'date', 'time']
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")
    
    try:
        booking = Booking(**data)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Failed to save booking: {str(e)}") from e

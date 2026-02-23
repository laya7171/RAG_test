from sqlalchemy.orm import Session
from db.models import Booking

def save_booking(db: Session, data):
    booking = Booking(**data)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

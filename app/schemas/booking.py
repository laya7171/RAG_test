"""Pydantic schemas for booking API.

This module defines request and response models for interview booking.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class BookingRequest(BaseModel):
    """Request model for creating a booking.
    
    Attributes:
        name: Full name of the person booking the interview.
        email: Email address for confirmation.
        date: Interview date (YYYY-MM-DD format).
        time: Interview time (HH:MM format).
    """
    name: str = Field(
        ...,
        description="Full name of the person",
        min_length=1,
        max_length=100
    )
    email: EmailStr = Field(
        ...,
        description="Email address for confirmation"
    )
    date: str = Field(
        ...,
        description="Interview date in YYYY-MM-DD format",
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
    time: str = Field(
        ...,
        description="Interview time in HH:MM format",
        pattern=r"^\d{2}:\d{2}$"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "date": "2026-03-15",
                "time": "14:30"
            }
        }


class BookingResponse(BaseModel):
    """Response model for booking creation.
    
    Attributes:
        id: Unique identifier for the booking.
        name: Name of the person who booked.
        email: Email address.
        date: Interview date.
        time: Interview time.
        message: Confirmation message.
    """
    id: str = Field(..., description="Unique booking identifier")
    name: str = Field(..., description="Name of the person")
    email: str = Field(..., description="Email address")
    date: str = Field(..., description="Interview date")
    time: str = Field(..., description="Interview time")
    message: str = Field(..., description="Confirmation message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "booking_123e4567",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "date": "2026-03-15",
                "time": "14:30",
                "message": "Interview booked successfully"
            }
        }
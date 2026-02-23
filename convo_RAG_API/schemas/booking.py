from pydantic import BaseModel

class BookingReqest(BaseModel):
    name: str
    email: str
    date: str
    time: str
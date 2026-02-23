from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid


Base = declarative_base()

class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key= True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable= False)
    chunking_strategy = Column(String, nullable = False)
    uploaded_at = Column(DateTime, default = datetime.utcnow)


class ChunkRecord(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key = True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, nullable = False)
    chunk_index = Column(Integer, nullable = True)
    content = Column(Text, nullable = False)
    vector_id = Column(String, nullable = False)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key= True, default = lambda: str(uuid.uuid4()))
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    date = Column(String, nullable  = False)
    time = Column(String, nullable = False)

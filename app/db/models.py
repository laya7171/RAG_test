"""SQLAlchemy database models for the RAG system.

This module defines the database schema for storing document metadata,
text chunks, and interview bookings.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from typing import Optional


Base = declarative_base()


class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=False, index=True)
    chunking_strategy = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        """String representation of DocumentRecord."""
        return f"<DocumentRecord(id={self.id}, filename={self.filename})>"


class ChunkRecord(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    vector_id = Column(String, nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        """String representation of ChunkRecord."""
        return f"<ChunkRecord(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        """String representation of Booking."""
        return f"<Booking(id={self.id}, name={self.name}, email={self.email})>"

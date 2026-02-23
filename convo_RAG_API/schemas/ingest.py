"""Pydantic schemas for document ingestion API."""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal


class ChunkingStrategy(Enum):
    """Supported chunking strategies."""
    fixed = "fixed"
    sentence = "sentence"


class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    document_id: str = Field(..., description="Unique identifier for the ingested document")
    filename: str = Field(..., description="Original filename of the uploaded document")
    chunks_count: int = Field(..., description="Number of chunks created from the document")
    chunking_strategy: str = Field(..., description="Chunking strategy used")
    message: str = Field(..., description="Success message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "example.pdf",
                "chunks_count": 15,
                "chunking_strategy": "fixed",
                "message": "Document ingested successfully"
            }
        }
"""Document ingestion REST API endpoints.

This module provides API routes for uploading, processing, and storing
documents with their embeddings.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.session import get_db
from db.models import DocumentRecord, ChunkRecord
from services.chunking import fixed_chunk, sentence_chunk
from services.embedding import embed_text
from services.vector_store import upsert_vectors
from utils.text_extraction import extract_text_from_pdf
from schemas.ingest import IngestResponse
from core.config import settings
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(
    file: UploadFile = File(..., description="PDF or TXT file to ingest"),
    chunking_strategy: str = Form(..., description="Chunking strategy: 'fixed' or 'sentence'"),
    db: Session = Depends(get_db)
) -> IngestResponse:
    """Ingest a document: extract text, chunk, embed, and store.
    
    This endpoint handles the complete document ingestion pipeline:
    1. Validates file type and chunking strategy
    2. Extracts text from the uploaded file
    3. Chunks the text according to the selected strategy
    4. Generates embeddings for each chunk
    5. Stores embeddings in Pinecone vector database
    6. Saves metadata to the SQL database
    
    Args:
        file: The uploaded PDF or TXT file.
        chunking_strategy: Strategy to use for text chunking ('fixed' or 'sentence').
        db: Database session (injected by FastAPI).
    
    Returns:
        IngestResponse containing document ID, filename, chunk count, and status.
    
    Raises:
        HTTPException 400: If file type or chunking strategy is invalid.
        HTTPException 413: If file size exceeds maximum allowed.
        HTTPException 500: If processing, embedding, or storage fails.
    """
    # Validate file extension
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    file_extension = file.filename.lower().split('.')[-1]
    if f".{file_extension}" not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {', '.join(settings.ALLOWED_EXTENSIONS)} files are supported"
        )
    
    # Validate chunking strategy
    valid_strategies = ["fixed", "sentence"]
    if chunking_strategy not in valid_strategies:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"chunking_strategy must be one of: {', '.join(valid_strategies)}"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum of {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # Extract text
        logger.info(f"Extracting text from {file.filename}")
        text = extract_text_from_pdf(content, file.filename)
        
        if not text or not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text content could be extracted from the file"
            )
        
        # Chunk text
        logger.info(f"Chunking text using '{chunking_strategy}' strategy")
        chunks: List[str] = (
            fixed_chunk(text) if chunking_strategy == "fixed" 
            else sentence_chunk(text)
        )
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No chunks were generated from the text"
            )
        
        # Create document record
        doc = DocumentRecord(
            filename=file.filename,
            chunking_strategy=chunking_strategy
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        logger.info(f"Created document record with ID: {doc.id}")
        
        # Process each chunk: embed and store
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue  # Skip empty chunks
            
            try:
                # Generate unique vector ID
                vector_id = f"{doc.id}_chunk_{i}_{str(uuid.uuid4())[:8]}"
                
                # Generate embedding
                embedding = embed_text(chunk)
                
                # Store in vector database
                upsert_vectors(
                    vector_id=vector_id,
                    embedding=embedding,
                    metadata={
                        "text": chunk,
                        "document_id": doc.id,
                        "chunk_index": i,
                        "filename": file.filename
                    }
                )
                
                # Store chunk metadata in database
                db_chunk = ChunkRecord(
                    document_id=doc.id,
                    chunk_index=i,
                    content=chunk,
                    vector_id=vector_id
                )
                db.add(db_chunk)
            
            except Exception as e:
                logger.error(f"Failed to process chunk {i}: {e}")
                continue
        
        # Commit all chunk records
        db.commit()
        
        logger.info(f"Successfully ingested document {doc.id} with {len(chunks)} chunks")
        
        return IngestResponse(
            document_id=doc.id,
            filename=file.filename,
            chunks_count=len(chunks),
            chunking_strategy=chunking_strategy,
            message="Document ingested successfully"
        )
    
    except HTTPException:
        raise
    
    except SQLAlchemyError as e:
        logger.error(f"Database error during ingestion: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while storing document"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during ingestion: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {str(e)}"
        )


@router.get("/documents", status_code=status.HTTP_200_OK)
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """List all ingested documents with pagination.
    
    Args:
        skip: Number of records to skip (for pagination).
        limit: Maximum number of records to return.
        db: Database session (injected by FastAPI).
    
    Returns:
        List of document records with their metadata.
    """
    try:
        documents = db.query(DocumentRecord).offset(skip).limit(limit).all()
        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "chunking_strategy": doc.chunking_strategy,
                "uploaded_at": doc.uploaded_at.isoformat()
            }
            for doc in documents
        ]
    except SQLAlchemyError as e:
        logger.error(f"Database error while listing documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve documents"
        )
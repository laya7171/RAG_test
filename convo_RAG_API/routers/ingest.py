from typing import Generator
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import sessionLocal
from db.models import DocumentRecord, ChunkRecord
from services.chunking import fixed_chunk, sentence_chunk
from services.embedding import embed_text
from services.vector_store import upsert_vectors
from utils.text_extraction import extract_text_from_pdf
from schemas.ingest import IngestResponse
import uuid

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()

@router.post("/", response_model=IngestResponse)
async def ingest(
    file: UploadFile = File(..., description="PDF or TXT file to ingest"),
    chunking_strategy: str = Form(..., description="Chunking strategy: 'fixed' or 'sentence'"),
    db: Session = Depends(get_db)
) -> IngestResponse:
    """Ingest a document: extract text, chunk, embed, and store."""
    # Validate file type
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")
    
    # Validate chunking strategy
    if chunking_strategy not in ["fixed", "sentence"]:
        raise HTTPException(status_code=400, detail="chunking_strategy must be 'fixed' or 'sentence'")
    
    content = await file.read()
    text = extract_text_from_pdf(content, file.filename)

    chunks = fixed_chunk(text) if chunking_strategy == "fixed" else sentence_chunk(text)
    doc = DocumentRecord(filename = file.filename, chunking_strategy = chunking_strategy)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    for i, chunk in enumerate(chunks):
        vector_id = str(uuid.uuid4())
        embedding = embed_text(chunk)
        upsert_vectors(vector_id, embedding, {"text": chunk})

        db_chunk = ChunkRecord(
            document_id = doc.id,
            chunk_index = i, 
            content = chunk,
            vector_id = vector_id
        )
        db.add(db_chunk)
    db.commit()

    return {
        "document_id": doc.id,
        "filename": file.filename,
        "chunks_count": len(chunks),
        "chunking_strategy": chunking_strategy,
        "message": "Document ingested successfully"
    }
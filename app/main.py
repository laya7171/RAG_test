from typing import Dict, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import ingest, chat
from db.models import Base
from db.session import engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Conversational RAG API",
    description="API for document ingestion, conversational RAG, and interview booking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    logger.info("Starting up application...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


@app.on_event("shutdown")
def shutdown() -> None:
    logger.info("Shutting down application...")


@app.get("/", response_class=JSONResponse)
def root() -> Dict[str, Any]:
    return {
        "message": "Conversational RAG API is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "ingest": "/ingest",
            "chat": "/chat"
        },
        "features": [
            "Document ingestion (PDF/TXT)",
            "Multiple chunking strategies",
            "Vector storage (Pinecone)",
            "Conversational RAG",
            "Redis-based memory",
            "Interview booking support"
        ]
    }


@app.get("/health", response_class=JSONResponse)
def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "Conversational RAG API"}


# Include routers
app.include_router(
    ingest.router,
    prefix="/ingest",
    tags=["Document Ingestion"]
)

app.include_router(
    chat.router,
    prefix="/chat",
    tags=["Conversational RAG"]
)
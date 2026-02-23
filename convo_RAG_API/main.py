from fastapi import FastAPI
from routers import ingest, chat
from db.models import Base
from db.session import engine

app = FastAPI(title = "Convo RAG API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Convo RAG API is running",
        "endpoints": {
            "docs": "/docs",
            "ingest": "/ingest",
            "chat": "/chat"
        }
    }

app.include_router(ingest.router, prefix = "/ingest", tags = ["Ingestion"])
app.include_router(chat.router, prefix = "/chat", tags = ["Chat"])
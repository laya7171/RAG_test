"""Application runner for the Conversational RAG API.

This script starts the FastAPI application using Uvicorn ASGI server.
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info")
    
    print("=" * 60)
    print("🚀 Starting Conversational RAG API")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Reload mode: {reload}")
    print(f"Log level: {log_level}")
    print("-" * 60)
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"📊 ReDoc: http://{host}:{port}/redoc")
    print(f"🏥 Health Check: http://{host}:{port}/health")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        access_log=True
    )

# Conversational RAG API

A production-ready REST API for document ingestion, conversational Q&A with Retrieval-Augmented Generation (RAG), and interview booking support using FastAPI.

## 🎯 Features

### Document Ingestion API

- ✅ Upload PDF and TXT files
- ✅ Multiple chunking strategies (fixed-size, sentence-based)
- ✅ Generate embeddings using OpenAI
- ✅ Store embeddings in Pinecone vector database
- ✅ Save metadata in SQL database (SQLite/PostgreSQL/MySQL)

### Conversational RAG API

- ✅ Custom RAG implementation (no RetrievalQAChain)
- ✅ Redis-based chat memory for multi-turn conversations
- ✅ Context-aware responses using conversation history
- ✅ Interview booking support with LLM-based extraction
- ✅ Store booking information in database

### Code Quality

- ✅ Clean, modular architecture
- ✅ Comprehensive type hints and annotations
- ✅ Industry-standard docstrings
- ✅ Robust error handling
- ✅ Production-ready logging

## 🏗️ Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── run.py                  # Application runner
├── core/
│   ├── config.py          # Configuration management
│   └── dependencies.py    # Shared dependencies
├── db/
│   ├── models.py          # SQLAlchemy models
│   └── session.py         # Database session management
├── routers/
│   ├── chat.py            # Chat endpoints
│   └── ingest.py          # Document ingestion endpoints
├── schemas/
│   ├── booking.py         # Booking schemas
│   ├── chat.py            # Chat schemas
│   └── ingest.py          # Ingestion schemas
├── services/
│   ├── booking.py         # Booking service
│   ├── chunking.py        # Text chunking strategies
│   ├── embedding.py       # Embedding generation
│   ├── llm_service.py     # LLM integration
│   ├── memory.py          # Redis-based memory
│   ├── rag.py             # Custom RAG pipeline
│   └── vector_store.py    # Pinecone integration
└── utils/
    └── text_extraction.py # PDF/TXT text extraction
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Redis server
- Pinecone account
- OpenAI API key
- Ollama (for local LLM) or OpenAI account

### Installation

1. **Clone and navigate to the project:**

```bash
cd app
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r ../requirements.txt
```

4. **Configure environment variables:**

```bash
cp .env.example .env
# Edit .env with your actual values
```

### Environment Configuration

Create a `.env` file with the following variables:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX=rag-index
PINECONE_ENVIRONMENT=us-east-1-aws

# Redis
REDIS_URL=redis://localhost:6379

# Database
DATABASE_URL=sqlite:///./rag.db
```

### Setup Pinecone Index

Before running the API, create a Pinecone index:

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

pc.create_index(
    name="rag-index",
    dimension=1536,  # text-embedding-3-small dimension
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
```

### Start Redis

```bash
# Linux/Mac
redis-server

# Windows (with Redis installed)
redis-server.exe

# Using Docker
docker run -d -p 6379:6379 redis:latest
```

### Install Ollama (Optional)

For local LLM support:

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
```

## 🏃 Running the Application

### Start the server:

```bash
python run.py
```

The API will be available at:

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Document Ingestion

#### Upload Document

```bash
POST /ingest/

curl -X POST "http://localhost:8000/ingest/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "chunking_strategy=fixed"
```

**Parameters:**

- `file`: PDF or TXT file (required)
- `chunking_strategy`: "fixed" or "sentence" (required)

**Response:**

```json
{
  "document_id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "document.pdf",
  "chunks_count": 15,
  "chunking_strategy": "fixed",
  "message": "Document ingested successfully"
}
```

#### List Documents

```bash
GET /ingest/documents?skip=0&limit=10

curl -X GET "http://localhost:8000/ingest/documents?skip=0&limit=10"
```

### Conversational Chat

#### Send Message

```bash
POST /chat/

curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "query": "What is the main topic of the document?"
  }'
```

**Request:**

```json
{
  "session_id": "user123",
  "query": "What is the main topic?"
}
```

**Response:**

```json
{
  "answer": "Based on the uploaded documents, the main topic is..."
}
```

#### Get Chat History

```bash
GET /chat/history/{session_id}

curl -X GET "http://localhost:8000/chat/history/user123"
```

#### Clear Chat History

```bash
DELETE /chat/history/{session_id}

curl -X DELETE "http://localhost:8000/chat/history/user123"
```

### Interview Booking

The chat endpoint automatically detects booking intent and extracts information:

```bash
# Example conversation for booking
POST /chat/
{
  "session_id": "user123",
  "query": "I'd like to book an interview for John Doe at john@example.com on March 15, 2026 at 2:30 PM"
}
```

The system will:

1. Detect booking intent
2. Extract: name, email, date, time
3. Save to database
4. Confirm in response

## 🔧 Chunking Strategies

### Fixed-Size Chunking

- Splits text into fixed character-length chunks
- Default: 400 characters with 40-character overlap
- Best for: Uniform processing, consistent chunk sizes

### Sentence-Based Chunking

- Splits text at sentence boundaries
- Groups sentences together (default: 5 sentences per chunk)
- Best for: Maintaining semantic coherence

## 🧪 Testing

### Test Document Ingestion

```python
import requests

with open("test.pdf", "rb") as f:
    files = {"file": f}
    data = {"chunking_strategy": "fixed"}
    response = requests.post(
        "http://localhost:8000/ingest/",
        files=files,
        data=data
    )
    print(response.json())
```

### Test Chat

```python
import requests

response = requests.post(
    "http://localhost:8000/chat/",
    json={
        "session_id": "test_session",
        "query": "What is this document about?"
    }
)
print(response.json())
```

## 📊 Database Schema

### Documents Table

- `id`: UUID primary key
- `filename`: Original filename
- `chunking_strategy`: Strategy used
- `uploaded_at`: Timestamp

### Chunks Table

- `id`: UUID primary key
- `document_id`: Foreign key to documents
- `chunk_index`: Sequential index
- `content`: Text content
- `vector_id`: Pinecone vector ID

### Bookings Table

- `id`: UUID primary key
- `name`: Person's name
- `email`: Email address
- `date`: Interview date
- `time`: Interview time
- `created_at`: Timestamp

## 🔒 Security Considerations

- Store API keys in `.env` (never commit to version control)
- Validate file types and sizes before processing
- Implement rate limiting for production
- Use HTTPS in production
- Add authentication/authorization as needed
- Configure CORS appropriately

## 🚀 Production Deployment

### Using PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
```

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

CMD ["python", "run.py"]
```

### Environment Variables for Production

```env
HOST=0.0.0.0
PORT=8000
RELOAD=false
LOG_LEVEL=warning
MAX_UPLOAD_SIZE=52428800  # 50MB
```

## 📈 Performance Tips

1. **Batch Embeddings**: Use `embed_texts_batch()` for multiple chunks
2. **Connection Pooling**: Configure database pool size
3. **Redis Optimization**: Adjust TTL based on usage patterns
4. **Async Processing**: Consider background tasks for large documents
5. **Caching**: Add Redis caching for frequently accessed data

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow existing code style
2. Add type hints to all functions
3. Include docstrings
4. Write tests for new features
5. Update documentation

## 📝 License

MIT License

## 🆘 Troubleshooting

### Redis Connection Error

- Ensure Redis server is running: `redis-cli ping`
- Check REDIS_URL in `.env`

### Pinecone Error

- Verify API key and index name
- Ensure index dimension matches embedding model (1536 for text-embedding-3-small)

### OpenAI API Error

- Check API key validity
- Verify account has credits
- Check rate limits

### Import Errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment

## 📧 Support

For issues or questions, please open an issue on the project repository.

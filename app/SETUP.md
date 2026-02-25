# Quick Setup Guide - Conversational RAG API

## 🚀 Quick Start (5 Minutes)

### Step 1: Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check if Redis is available
redis-cli ping  # Should return "PONG"

# If Redis not installed:
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Mac: brew install redis
# Linux: sudo apt-get install redis-server
```

### Step 2: Install Dependencies

```bash
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# Minimum required:
# - OPENAI_API_KEY
# - PINECONE_API_KEY
# - PINECONE_INDEX
```

### Step 4: Setup Pinecone Index

```python
# Run this Python script once
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-pinecone-key")

pc.create_index(
    name="rag-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
```

### Step 5: Start Redis

```bash
# In a separate terminal
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis:latest
```

### Step 6: Install Ollama (Optional)

```bash
# Download from https://ollama.ai
ollama pull llama3.2
```

### Step 7: Run the API

```bash
python run.py
```

Visit http://localhost:8000/docs for interactive API documentation!

## 🧪 Test the API

### Test 1: Upload a Document

```bash
# Create a test file
echo "Artificial Intelligence is transforming healthcare." > test.txt

# Upload it
curl -X POST "http://localhost:8000/ingest/" \
  -F "file=@test.txt" \
  -F "chunking_strategy=fixed"
```

### Test 2: Chat with the Document

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "query": "What is AI doing in healthcare?"
  }'
```

### Test 3: Book an Interview

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test123",
    "query": "I want to book an interview for John Doe, email john@example.com, on March 15, 2026 at 2:30 PM"
  }'
```

## 🐛 Troubleshooting

### Redis Connection Failed

```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
redis-server
```

### Pinecone Error

- Verify your API key in .env
- Check if index exists: https://app.pinecone.io/
- Ensure dimension is 1536 for text-embedding-3-small

### OpenAI API Error

- Check API key in .env
- Verify account has credits: https://platform.openai.com/usage
- Check rate limits

### Import Errors

```bash
# Reinstall dependencies
pip install -r ../requirements.txt --upgrade
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the API at http://localhost:8000/docs
3. Upload your own PDF documents
4. Test multi-turn conversations
5. Try the booking feature

## 🎯 Success Checklist

- [ ] Python 3.8+ installed
- [ ] Redis server running
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Pinecone index created
- [ ] Ollama installed (optional)
- [ ] API running at http://localhost:8000
- [ ] Test document uploaded successfully
- [ ] Chat response received
- [ ] Booking extracted and saved

## 💡 Tips

1. **Use the Interactive Docs**: Visit `/docs` for easy testing
2. **Monitor Logs**: Watch the terminal for debugging info
3. **Check Redis**: Use `redis-cli` to inspect stored data
4. **Pinecone Console**: Monitor vector operations at pinecone.io
5. **Database**: Check `rag.db` with SQLite browser

## 🆘 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review error messages in the terminal
- Check the logs for detailed error information
- Ensure all environment variables are set correctly

---

**Ready to go!** 🚀 Your Conversational RAG API is now fully functional!

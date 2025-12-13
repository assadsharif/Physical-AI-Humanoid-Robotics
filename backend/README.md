# RAG Chatbot Backend

FastAPI backend for the Physical AI & Humanoid Robotics textbook RAG chatbot.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_URL` - Qdrant Cloud cluster URL
- `QDRANT_API_KEY` - Qdrant authentication key
- `DATABASE_URL` - Neon Postgres connection string

### 3. Set Up External Services

#### Qdrant Cloud (Vector Database)
1. Create account at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a new cluster (free tier available)
3. Copy the cluster URL and API key to `.env`

#### Neon Postgres (Conversation Storage)
1. Create account at [neon.tech](https://neon.tech)
2. Create a new project (free tier available)
3. Copy the connection string to `.env`

#### OpenAI API
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Ensure you have access to GPT-4 and text-embedding-ada-002
3. Copy the API key to `.env`

### 4. Ingest Content

Run the ingestion script to populate the vector database:

```bash
# Dry run (no upload)
python scripts/ingest_content.py --docs-path ../my-project/docs --dry-run

# Full ingestion
python scripts/ingest_content.py --docs-path ../my-project/docs
```

### 5. Start the Server

```bash
# Development mode
uvicorn src.main:app --reload --port 8000

# Production mode
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/chat
Process a chat query and return RAG-generated response.

```json
{
  "query": "What is Zero Moment Point?",
  "session_id": "uuid-string",
  "selected_text": null,
  "page_context": {
    "chapter_id": "ch19",
    "url": "/docs/part-v-control/ch19-bipedal-locomotion"
  }
}
```

### GET /api/search
Direct vector similarity search.

```
GET /api/search?q=bipedal+locomotion&limit=5
```

### GET /api/health
Service health check.

## Project Structure

```
backend/
├── src/
│   ├── api/routes/      # FastAPI route handlers
│   ├── core/            # Configuration and prompts
│   ├── models/          # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── scripts/
│   └── ingest_content.py  # Content ingestion
├── requirements.txt
└── .env.example
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format
black src/ scripts/

# Lint
ruff src/ scripts/
```

## Deployment

### Docker

```bash
docker build -t rag-chatbot-backend .
docker run -p 8000:8000 --env-file .env rag-chatbot-backend
```

### Environment Variables for Production

Set these additional variables for production:
- `APP_ENV=production`
- `DEBUG=false`
- `CORS_ORIGINS=https://your-site.com`

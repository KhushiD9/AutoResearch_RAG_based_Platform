# Backend - Research Paper Assistant API

FastAPI-based backend for the AI-powered research paper assistant.

## Features

- Paper discovery from Semantic Scholar and arXiv
- PDF processing and text extraction
- Vector embeddings generation
- RAG-based question answering
- Multiple query modes
- History tracking

## Installation

1. Create virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```cmd
pip install -r requirements.txt
```

3. Configure environment:
```cmd
copy .env.example .env
```

Edit `.env` with your API keys.

4. Run the server:
```cmd
python main.py
```

Server runs at: http://localhost:8000
API docs: http://localhost:8000/docs

## Project Structure

```
backend/
├── api/
│   └── routes/          # API endpoint definitions
├── services/            # Business logic
├── config.py            # Configuration
├── main.py              # Application entry point
└── requirements.txt     # Dependencies
```

## API Documentation

Once running, visit http://localhost:8000/docs for interactive API documentation.

## Environment Variables

Required:
- `GEMINI_API_KEY` - Google Gemini API key (get from https://makersuite.google.com)

Optional:
- `OPENAI_API_KEY` - OpenAI API key (for alternative LLM)
- `DATABASE_URL` - PostgreSQL connection (for persistent storage)

## Development

Run in development mode with auto-reload:
```cmd
uvicorn main:app --reload
```

## Testing

Test the API endpoints using the Swagger UI at `/docs` or with curl:

```cmd
curl -X POST http://localhost:8000/api/papers/search -H "Content-Type: application/json" -d "{\"topic\": \"machine learning\", \"limit\": 5}"
```

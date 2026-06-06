# Research Paper Assistant — Quickstart

## 1. Backend setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Open .env and set: ANTHROPIC_API_KEY=sk-ant-...

# Run the server
python main.py
# Backend available at http://localhost:8000
# API docs at       http://localhost:8000/docs
```

## 2. Frontend setup

```bash
cd frontend
npm install
ng serve
# Frontend available at http://localhost:4200
```

## 3. Using the app

1. Open http://localhost:4200
2. Go to **Search** — enter a topic like "anti-pinch controller"
3. Wait for the pipeline to complete (PDF download → chunk → embed → ChromaDB)
4. Go to **Chat** — select the collection, ask questions
5. Switch modes: Q&A / Compare / Literature Review / Research Gaps

## Notes

- Embeddings use **all-MiniLM-L6-v2** (local, free — first run downloads ~90 MB)
- LLM uses **Claude Haiku** via Anthropic API (fast + cost-efficient)
- Vector store uses **ChromaDB** persisted to `./backend/chroma_db/`
- No PostgreSQL needed — history is in-memory

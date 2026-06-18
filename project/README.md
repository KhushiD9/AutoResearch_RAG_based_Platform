# AutoResearch : AI-Powered Research Paper Assistant

> A AI application that automatically discovers, analyzes, and answers questions from scientific papers using Retrieval-Augmented Generation (RAG)

- [Installation Guide](INSTALLATION_GUIDE.md) - Detailed setup
- [Quick Start](QUICKSTART.md) - 5-minute setup
- [Features](FEATURES.md) - What it can do
- [API Docs](API_DOCUMENTATION.md) - API reference

## Features

- **Paper Discovery**: Search and retrieve open-access research papers from Semantic Scholar and arXiv APIs
- **Intelligent Processing**: Automatic PDF download, text extraction, and chunking
- **Vector Storage**: Store paper embeddings in ChromaDB for efficient retrieval
- **RAG Pipeline**: Retrieve relevant paper sections and generate contextual answers using LLMs
- **Multiple Query Modes**:
  - Standard Q&A
  - Paper Comparison
  - Literature Review Generation
  - Research Gap Identification
- **Citation-Backed Responses**: All answers include source references
- **Query History**: Track and review previous research questions
- **Modern Glassmorphism UI**: Beautiful, responsive Angular interface

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Semantic Scholar API**: Academic paper discovery
- **arXiv API**: Open-access paper repository
- **PyPDF2 & pdfplumber**: PDF text extraction
- **ChromaDB**: Vector database for embeddings
- **LangChain**: RAG pipeline orchestration
- **Google Gemini / OpenAI**: Embeddings and answer generation

### Frontend
- **Angular 17**: Modern TypeScript framework
- **RxJS**: Reactive programming
- **SCSS**: Advanced styling with glassmorphism design
- **Responsive Design**: Mobile-first approach

## Project Structure

```
ai-research-assistant/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── paper_routes.py      # Paper search and indexing
│   │       ├── chat_routes.py       # Question answering
│   │       └── history_routes.py    # Query history
│   ├── services/
│   │   ├── paper_discovery.py       # Paper search service
│   │   ├── pdf_processor.py         # PDF download and processing
│   │   ├── embeddings.py            # Embedding generation
│   │   ├── vector_store.py          # ChromaDB operations
│   │   ├── llm_service.py           # LLM integration
│   │   └── rag_pipeline.py          # Complete RAG workflow
│   ├── config.py                    # Configuration management
│   ├── main.py                      # FastAPI application
│   └── requirements.txt             # Python dependencies
│
└── frontend/
    └── src/
        ├── app/
        │   ├── components/
        │   │   ├── search/          # Paper search interface
        │   │   ├── chat/            # Question interface
        │   │   ├── history/         # History viewer
        │   │   ├── header/          # Navigation header
        │   │   └── loader/          # Loading indicator
        │   ├── services/
        │   │   ├── api.service.ts   # API client
        │   │   └── state.service.ts # State management
        │   └── app.module.ts
        ├── styles.scss              # Global glassmorphism styles
        └── index.html
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```cmd
cd backend
```

2. Create a virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Create a `.env` file:
```cmd
copy .env.example .env
```

5. Edit `.env` and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Get API keys from:
- Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

6. Run the backend server:
```cmd
python main.py
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```cmd
cd frontend
```

2. Install dependencies:
```cmd
npm install
```

3. Start the development server:
```cmd
npm start
```

The application will be available at `http://localhost:4200`

## Usage Guide

### 1. Search for Papers

1. Navigate to the "Search Papers" page
2. Enter a research topic (e.g., "anti-pinch controller", "machine learning", "quantum computing")
3. Select the number of papers to process (3, 5, or 10)
4. Choose your preferred AI provider (Gemini or OpenAI)
5. Click "Search Papers"

The system will:
- Search Semantic Scholar and arXiv for relevant papers
- Download available PDFs
- Extract and chunk the text
- Generate embeddings
- Store everything in ChromaDB

### 2. Ask Questions

1. Navigate to the "Ask Questions" page
2. Select a paper collection from the sidebar
3. Choose a query mode:
   - **Q&A**: Standard question answering
   - **Compare**: Compare multiple papers
   - **Review**: Generate a literature review
   - **Gaps**: Identify research gaps
4. Type your question and press Enter or click Send

Example questions:
- "What are the main findings in these papers?"
- "How do these approaches compare?"
- "What are the key methodologies used?"
- "What research gaps exist in this area?"

### 3. View History

1. Navigate to the "History" page
2. Browse your previous questions and answers
3. Delete individual entries or clear all history

## API Endpoints

### Paper Management
- `POST /api/papers/search` - Search and index papers
- `GET /api/papers/collections` - List all collections
- `DELETE /api/papers/collections/{name}` - Delete a collection

### Question Answering
- `POST /api/chat/query` - Ask a question
- `POST /api/chat/compare` - Compare papers
- `POST /api/chat/literature-review` - Generate review
- `POST /api/chat/research-gaps` - Identify gaps

### History
- `POST /api/history/save` - Save query to history
- `GET /api/history/list` - Get history
- `DELETE /api/history/{id}` - Delete entry
- `DELETE /api/history/clear` - Clear all history

## Configuration

### Backend Configuration
Edit `backend/config.py` to modify:
- API keys
- Database URL
- Token expiration
- Other settings

### Frontend Configuration
Edit `frontend/src/app/services/api.service.ts` to change the backend URL if needed:
```typescript
private baseUrl = 'http://localhost:8000/api';
```

## Design - Glassmorphism UI

The interface features a modern glassmorphism design with:
- Frosted glass effect cards
- Smooth animations and transitions
- Gradient backgrounds
- Responsive layout
- Accessible color contrasts
- Custom scrollbars

## Troubleshooting

### Backend Issues

**ChromaDB errors:**
- Ensure the `chroma_db` directory has write permissions
- Delete and recreate if corrupted

**PDF download failures:**
- Some papers may not have open-access PDFs
- Check network connectivity
- Some publishers block automated downloads

**API rate limits:**
- Semantic Scholar has rate limits
- Add delays between requests if needed

**LLM API errors:**
- Verify API keys are correct
- Check API quota and billing
- Ensure proper network access

### Frontend Issues

**CORS errors:**
- Ensure backend is running on port 8000
- Check CORS configuration in `main.py`

**Build errors:**
- Clear `node_modules` and reinstall
- Check Node.js version compatibility

## Future Enhancements

- PostgreSQL integration for persistent storage
- User authentication and multi-user support
- PDF annotation and highlighting
- Export results to PDF/Word
- Advanced filtering and sorting
- Paper recommendation system
- Citation network visualization
- Batch processing capabilities
- Custom embedding models
- Multi-language support

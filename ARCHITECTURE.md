# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                     (Angular Frontend)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Search  │  │   Chat   │  │ History  │  │  Header  │      │
│  │   Page   │  │   Page   │  │   Page   │  │Component │      │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘      │
│       │             │              │                            │
│       └─────────────┴──────────────┘                            │
│                     │                                            │
│              ┌──────▼──────┐                                    │
│              │ API Service │                                    │
│              └──────┬──────┘                                    │
└─────────────────────┼───────────────────────────────────────────┘
                      │ HTTP/REST API
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                    FastAPI Backend                              │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                   API Routes Layer                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Paper   │  │   Chat   │  │ History  │            │   │
│  │  │  Routes  │  │  Routes  │  │  Routes  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼─────────────┼─────────────┼──────────────────┘   │
│          │             │             │                         │
│  ┌───────▼─────────────▼─────────────▼──────────────────┐   │
│  │              RAG Pipeline Service                      │   │
│  │         (Orchestrates all operations)                  │   │
│  └───────┬───────────────────┬───────────────┬──────────┘   │
│          │                   │               │                │
│  ┌───────▼────────┐  ┌───────▼───────┐  ┌──▼─────────┐     │
│  │     Paper      │  │      PDF      │  │ Embeddings │     │
│  │   Discovery    │  │   Processor   │  │  Service   │     │
│  │    Service     │  │               │  │            │     │
│  └───────┬────────┘  └───────┬───────┘  └──┬─────────┘     │
│          │                   │              │                │
│  ┌───────▼────────┐  ┌───────▼───────┐  ┌─▼──────────┐    │
│  │  Vector Store  │  │  LLM Service  │  │   Config   │    │
│  │   (ChromaDB)   │  │  (Gemini/GPT) │  │  Manager   │    │
│  └────────────────┘  └───────────────┘  └────────────┘    │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│               External Services & Storage                   │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Semantic  │  │  arXiv   │  │  Gemini  │  │ ChromaDB │  │
│  │ Scholar  │  │   API    │  │   API    │  │  Storage │  │
│  │   API    │  │          │  │          │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Paper Discovery & Indexing Flow

```
User Input: "machine learning"
         │
         ▼
    Search Component
         │
         ▼
    POST /api/papers/search
         │
         ▼
    RAG Pipeline.index_papers()
         │
    ┌────┴────┐
    ▼         ▼
Semantic   arXiv
Scholar     API
    │         │
    └────┬────┘
         ▼
    Paper Discovery Service
         │
         ▼
   [Paper Metadata]
         │
         ▼
    PDF Processor
         │
    ┌────┴────┐
    ▼         ▼
Download   Extract
  PDFs      Text
    │         │
    └────┬────┘
         ▼
    Text Chunking
         │
         ▼
   [Text Chunks]
         │
         ▼
   Embeddings Service
         │
    ┌────┴────┐
    ▼         ▼
  Gemini   OpenAI
embedding-001  ada-002
    │         │
    └────┬────┘
         ▼
   [Vector Embeddings]
         │
         ▼
    Vector Store (ChromaDB)
         │
         ▼
  Collection Saved
         │
         ▼
    Return to Frontend
```

### 2. Question Answering Flow

```
User Question: "What are the main findings?"
         │
         ▼
    Chat Component
         │
         ▼
    POST /api/chat/query
         │
         ▼
    RAG Pipeline.query()
         │
         ▼
   Embeddings Service
         │
         ▼
   [Query Embedding]
         │
         ▼
    Vector Store
    Similarity Search
         │
         ▼
   [Top 5 Relevant Chunks]
         │
         ▼
    LLM Service
    (with context)
         │
    ┌────┴────┐
    ▼         ▼
  Gemini    GPT-4
   Pro     Turbo
    │         │
    └────┬────┘
         ▼
   [Generated Answer]
         │
         ▼
  Return with Sources
         │
         ▼
    Display in Chat
         │
         ▼
    Save to History
```

---

## Component Responsibilities

### Frontend Components

#### Search Component
**Purpose**: Paper discovery interface
**Inputs**: Topic, limit, provider
**Outputs**: Collection name, processed papers
**State**: Loading, error, results

#### Chat Component
**Purpose**: Question answering interface
**Inputs**: Collection, question, mode
**Outputs**: Answer with sources
**State**: Messages array, loading

#### History Component
**Purpose**: Query history viewer
**Inputs**: None (loads from API)
**Outputs**: Display history entries
**State**: History array, loading

### Backend Services

#### Paper Discovery Service
**Purpose**: Search for papers
**APIs Used**: Semantic Scholar, arXiv
**Returns**: Paper metadata with PDF URLs

#### PDF Processor
**Purpose**: Download and extract text
**Methods**: PyPDF2 (primary), pdfplumber (fallback)
**Returns**: Extracted text and chunks

#### Embeddings Service
**Purpose**: Generate vector embeddings
**Models**: Gemini embedding-001, OpenAI ada-002
**Returns**: Float vectors (768 or 1536 dimensions)

#### Vector Store
**Purpose**: Manage ChromaDB operations
**Operations**: Add, query, delete, list
**Returns**: Similar documents with metadata

#### LLM Service
**Purpose**: Generate contextual answers
**Models**: Gemini Pro, GPT-4 Turbo
**Returns**: Natural language responses

#### RAG Pipeline
**Purpose**: Orchestrate complete workflow
**Coordinates**: All other services
**Returns**: Complete results

---

## Technology Stack Details

### Frontend Stack

```
Angular 17
    │
    ├── TypeScript 5.2
    │   └── Type safety, interfaces, decorators
    │
    ├── RxJS 7.8
    │   └── Observables, operators, reactive programming
    │
    ├── SCSS
    │   └── Variables, mixins, glassmorphism
    │
    └── Angular Router
        └── Navigation, lazy loading
```

### Backend Stack

```
FastAPI
    │
    ├── Uvicorn (ASGI Server)
    │
    ├── Pydantic (Validation)
    │
    ├── HTTPX (Async HTTP)
    │
    └── Services
        │
        ├── PDF Processing
        │   ├── PyPDF2
        │   └── pdfplumber
        │
        ├── Vector DB
        │   └── ChromaDB
        │
        ├── LLMs
        │   ├── Google Generative AI
        │   └── OpenAI
        │
        └── APIs
            ├── Semantic Scholar
            └── arXiv
```

---

## Database Schema

### Vector Store Collections

```
Collection: topic_machine_learning
│
├── Documents (text chunks)
│
├── Embeddings (vectors)
│
└── Metadata
    ├── paper_id
    ├── title
    ├── authors
    ├── year
    ├── chunk_id
    └── source
```

### History Storage (In-Memory)

```
History Entry
│
├── id (string)
├── collection_name (string)
├── question (string)
├── answer (string)
├── mode (string)
└── timestamp (datetime)
```

---

## Request/Response Flow

### Search Papers Request

```json
REQUEST:
POST /api/papers/search
{
  "topic": "machine learning",
  "limit": 5,
  "provider": "gemini"
}

RESPONSE:
{
  "success": true,
  "collection_name": "topic_machine_learning",
  "papers_found": 5,
  "papers_processed": 4,
  "processed_papers": [
    {
      "paper_id": "abc123",
      "title": "Deep Learning",
      "chunks_count": 87
    }
  ]
}
```

### Query Papers Request

```json
REQUEST:
POST /api/chat/query
{
  "collection_name": "topic_machine_learning",
  "question": "What are the main findings?",
  "n_results": 5,
  "mode": "standard"
}

RESPONSE:
{
  "success": true,
  "answer": "The main findings indicate...",
  "sources": [
    {
      "text": "Context chunk...",
      "metadata": {
        "paper_id": "abc123",
        "title": "Paper Title"
      }
    }
  ],
  "sources_count": 5
}
```

---

## Error Handling Strategy

```
User Action
    │
    ▼
Frontend Validation
    │
    ├── Valid → API Call
    │              │
    └── Invalid → Show Error
                   │
                   ▼
              API Request
                   │
                   ▼
              Backend Validation
                   │
                   ├── Valid → Process
                   │              │
                   └── Invalid → 422 Error
                                  │
                                  ▼
                             Service Layer
                                  │
                             ┌────┴────┐
                             ▼         ▼
                          Success   Exception
                             │         │
                             │         └── Log & Return Error
                             │
                             ▼
                        200 Response
                             │
                             ▼
                       Frontend Display
```

---

## Security Architecture

```
┌─────────────────────────────────────┐
│         Security Layers             │
├─────────────────────────────────────┤
│  1. Environment Variables           │
│     - API keys isolated             │
│     - .env not in git               │
├─────────────────────────────────────┤
│  2. Input Validation                │
│     - Pydantic models               │
│     - Type checking                 │
├─────────────────────────────────────┤
│  3. CORS Configuration              │
│     - Specific origins              │
│     - Controlled methods            │
├─────────────────────────────────────┤
│  4. Error Handling                  │
│     - No sensitive info in errors   │
│     - Structured logging            │
├─────────────────────────────────────┤
│  5. HTTPS Ready                     │
│     - SSL/TLS support               │
│     - Secure headers                │
└─────────────────────────────────────┘
```

---

## Scalability Path

### Current (MVP)
```
Single Server
    ├── FastAPI (1 instance)
    ├── Angular (static files)
    ├── ChromaDB (local)
    └── In-memory storage
```

### Production (Scaled)
```
Load Balancer
    │
    ├── App Servers (multiple)
    │   └── FastAPI instances
    │
    ├── Static Files (CDN)
    │   └── Angular build
    │
    ├── Vector DB (hosted)
    │   └── ChromaDB cluster
    │
    ├── Relational DB
    │   └── PostgreSQL
    │
    ├── Cache Layer
    │   └── Redis
    │
    └── Task Queue
        └── Celery workers
```

---

## Performance Characteristics

### Current Performance

| Operation | Time | Bottleneck |
|-----------|------|------------|
| Search 5 papers | 1-2 min | PDF download & processing |
| Generate embeddings | 10-30s | API rate limits |
| Query answering | 3-5s | LLM generation |
| Vector search | <100ms | ChromaDB |
| Frontend load | <1s | Static assets |

### Optimization Opportunities

1. **Parallel Processing** - Process multiple PDFs simultaneously
2. **Caching** - Cache frequent queries and embeddings
3. **Queue System** - Background processing for heavy tasks
4. **CDN** - Serve static assets faster
5. **Connection Pooling** - Reuse database connections

---

## Monitoring Points

```
Application Monitoring
    │
    ├── API Endpoints
    │   ├── Response times
    │   ├── Error rates
    │   └── Request counts
    │
    ├── External APIs
    │   ├── Semantic Scholar rate limits
    │   ├── arXiv availability
    │   └── LLM API usage
    │
    ├── Database
    │   ├── Query performance
    │   ├── Storage usage
    │   └── Connection pool
    │
    └── Application
        ├── Memory usage
        ├── CPU utilization
        └── Error logs
```

---

## Deployment Architecture

### Development
```
Developer Machine
    ├── Backend (localhost:8000)
    ├── Frontend (localhost:4200)
    └── ChromaDB (local files)
```

### Production
```
Cloud Infrastructure
    │
    ├── Web Server (Nginx)
    │   ├── Static files (Angular)
    │   └── Reverse proxy to API
    │
    ├── Application Server
    │   └── FastAPI (Uvicorn/Gunicorn)
    │
    ├── Vector Database
    │   └── ChromaDB (persistent volume)
    │
    └── Monitoring
        ├── Logs (centralized)
        └── Metrics (dashboard)
```

---

## API Documentation Access

```
Production API
    │
    └── /docs (Swagger UI)
        │
        ├── Interactive testing
        ├── Schema definitions
        ├── Request examples
        └── Response formats
```

---

This architecture enables:
- ✅ Scalability
- ✅ Maintainability
- ✅ Testability
- ✅ Security
- ✅ Performance
- ✅ Extensibility

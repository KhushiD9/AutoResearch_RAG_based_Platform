# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Interactive Documentation
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Authentication
Currently, no authentication is required. Future versions will implement JWT-based authentication.

---

## Paper Management Endpoints

### Search and Index Papers
Search for papers on a topic and index them in the vector database.

**Endpoint:** `POST /api/papers/search`

**Request Body:**
```json
{
  "topic": "machine learning",
  "limit": 5,
  "provider": "gemini"
}
```

**Parameters:**
- `topic` (string, required): Research topic to search for
- `limit` (integer, optional): Number of papers to retrieve (default: 5, max: 10)
- `provider` (string, optional): AI provider - "gemini" or "openai" (default: "gemini")

**Response (200 OK):**
```json
{
  "success": true,
  "collection_name": "topic_machine_learning",
  "papers_found": 5,
  "papers_processed": 4,
  "processed_papers": [
    {
      "paper_id": "abc123",
      "title": "Deep Learning Fundamentals",
      "chunks_count": 87
    }
  ]
}
```

**Response (500 Error):**
```json
{
  "success": false,
  "error": "No papers found for the given topic",
  "papers_processed": 0
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/papers/search \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing", "limit": 3}'
```

---

### List Collections
Get all available paper collections.

**Endpoint:** `GET /api/papers/collections`

**Response (200 OK):**
```json
{
  "success": true,
  "collections": [
    "topic_machine_learning",
    "topic_quantum_computing",
    "topic_neural_networks"
  ],
  "count": 3
}
```

**Example:**
```bash
curl http://localhost:8000/api/papers/collections
```

---

### Delete Collection
Remove a paper collection from the vector database.

**Endpoint:** `DELETE /api/papers/collections/{collection_name}`

**Parameters:**
- `collection_name` (string, path): Name of collection to delete

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Collection topic_machine_learning deleted successfully"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Collection not found"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/papers/collections/topic_machine_learning
```

---

## Chat/Query Endpoints

### Ask a Question
Query the indexed papers with a question.

**Endpoint:** `POST /api/chat/query`

**Request Body:**
```json
{
  "collection_name": "topic_machine_learning",
  "question": "What are the main findings?",
  "n_results": 5,
  "mode": "standard",
  "provider": "gemini"
}
```

**Parameters:**
- `collection_name` (string, required): Name of the collection to query
- `question` (string, required): Question to ask
- `n_results` (integer, optional): Number of context chunks to retrieve (default: 5)
- `mode` (string, optional): Query mode - see Query Modes section (default: "standard")
- `provider` (string, optional): AI provider (default: "gemini")

**Response (200 OK):**
```json
{
  "success": true,
  "answer": "The main findings indicate that...",
  "sources": [
    {
      "text": "Context chunk text...",
      "metadata": {
        "paper_id": "abc123",
        "title": "Paper Title",
        "authors": "John Doe, Jane Smith",
        "year": 2023,
        "chunk_id": 0,
        "source": "semantic_scholar"
      }
    }
  ],
  "sources_count": 5
}
```

**Response (500 Error):**
```json
{
  "success": false,
  "error": "No relevant documents found"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "topic_machine_learning",
    "question": "What methodologies were used?",
    "mode": "standard"
  }'
```

---

### Compare Papers
Compare multiple papers on a specific aspect.

**Endpoint:** `POST /api/chat/compare`

**Request Body:**
Same as `/api/chat/query` but mode is automatically set to "compare"

**Response:**
Same structure as `/api/chat/query`

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat/compare \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "topic_machine_learning",
    "question": "Compare the approaches used in these papers"
  }'
```

---

### Generate Literature Review
Create a literature review from indexed papers.

**Endpoint:** `POST /api/chat/literature-review`

**Request Body:**
Same as `/api/chat/query` but mode is automatically set to "literature_review"

**Response:**
Same structure as `/api/chat/query`

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat/literature-review \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "topic_machine_learning",
    "question": "Provide an overview of recent machine learning research"
  }'
```

---

### Identify Research Gaps
Find gaps in current research.

**Endpoint:** `POST /api/chat/research-gaps`

**Request Body:**
Same as `/api/chat/query` but mode is automatically set to "research_gaps"

**Response:**
Same structure as `/api/chat/query`

**Example:**
```bash
curl -X POST http://localhost:8000/api/chat/research-gaps \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "topic_machine_learning",
    "question": "What research gaps exist in this area?"
  }'
```

---

## History Endpoints

### Save History Entry
Save a query to history.

**Endpoint:** `POST /api/history/save`

**Request Body:**
```json
{
  "collection_name": "topic_machine_learning",
  "question": "What are the main findings?",
  "answer": "The main findings are...",
  "mode": "standard"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "History entry saved",
  "id": "1"
}
```

---

### Get History
Retrieve query history.

**Endpoint:** `GET /api/history/list?limit=50`

**Query Parameters:**
- `limit` (integer, optional): Maximum number of entries to return (default: 50)

**Response (200 OK):**
```json
{
  "success": true,
  "entries": [
    {
      "id": "1",
      "collection_name": "topic_machine_learning",
      "question": "What are the main findings?",
      "answer": "The main findings are...",
      "mode": "standard",
      "timestamp": "2026-06-04T20:30:00"
    }
  ],
  "count": 1
}
```

---

### Delete History Entry
Remove a single history entry.

**Endpoint:** `DELETE /api/history/{entry_id}`

**Parameters:**
- `entry_id` (string, path): ID of the entry to delete

**Response (200 OK):**
```json
{
  "success": true,
  "message": "History entry deleted"
}
```

---

### Clear All History
Remove all history entries.

**Endpoint:** `DELETE /api/history/clear`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "History cleared"
}
```

---

## Query Modes

### Standard Mode (`"standard"`)
**Purpose:** Direct question answering

**Best for:**
- Factual questions
- Specific information retrieval
- Quick answers

**Example Questions:**
- "What datasets were used?"
- "What are the main conclusions?"
- "How does this method work?"

---

### Compare Mode (`"compare"`)
**Purpose:** Side-by-side paper analysis

**Best for:**
- Methodology comparison
- Results comparison
- Approach analysis

**Example Questions:**
- "How do these papers differ in their approach?"
- "Which paper has better results?"
- "Compare the methodologies used"

---

### Literature Review Mode (`"literature_review"`)
**Purpose:** Comprehensive synthesis

**Best for:**
- Overview of research area
- Thematic analysis
- Trend identification

**Example Questions:**
- "Provide an overview of this field"
- "What are the key themes?"
- "Summarize the current state of research"

---

### Research Gaps Mode (`"research_gaps"`)
**Purpose:** Identify missing research

**Best for:**
- Finding unexplored areas
- Identifying contradictions
- Future research directions

**Example Questions:**
- "What hasn't been studied yet?"
- "What are the open questions?"
- "Where should future research focus?"

---

## Error Codes

### HTTP Status Codes

- `200 OK` - Request successful
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Invalid request parameters
- `500 Internal Server Error` - Server error

### Application Error Responses

All error responses follow this format:
```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common Errors:**

1. **No papers found**
   ```json
   {
     "success": false,
     "error": "No papers found for the given topic"
   }
   ```

2. **Failed to process PDF**
   ```json
   {
     "success": false,
     "error": "Failed to extract text from PDF"
   }
   ```

3. **No relevant documents**
   ```json
   {
     "success": false,
     "error": "No relevant documents found"
   }
   ```

4. **Collection not found**
   ```json
   {
     "detail": "Collection not found"
   }
   ```

---

## Rate Limits

Currently, no rate limits are enforced. Future versions will implement:
- 100 requests per minute per IP
- 1000 requests per day per user

---

## Best Practices

### 1. Collection Naming
Collections are automatically named: `topic_{sanitized_topic_name}`

### 2. Question Formulation
- Be specific and clear
- Use technical terminology when appropriate
- Ask one question at a time

### 3. Result Count
- Default `n_results=5` works well for most queries
- Increase for comprehensive answers
- Decrease for faster responses

### 4. Provider Selection
- Gemini: Free tier available, good quality
- OpenAI: Paid only, slightly better for complex queries

### 5. Error Handling
Always check the `success` field in responses:
```javascript
if (response.success) {
  // Handle success
} else {
  // Handle error with response.error
}
```

---

## Webhooks (Future)

Future versions will support webhooks for:
- Paper processing completion
- Query result notifications
- Collection updates

---

## Pagination (Future)

Future versions will support pagination for:
- History list
- Collection list
- Search results

Example:
```
GET /api/history/list?page=1&per_page=20
```

---

## Versioning

Current API version: `v1`

Future versions will use URL versioning:
```
http://localhost:8000/api/v2/papers/search
```

---

## WebSocket Support (Future)

Real-time updates via WebSocket for:
- Live query responses
- Processing progress
- Collection updates

---

## Examples

### Complete Workflow Example

```bash
# 1. Search for papers
curl -X POST http://localhost:8000/api/papers/search \
  -H "Content-Type: application/json" \
  -d '{"topic": "neural networks", "limit": 5}'

# Response: {"success": true, "collection_name": "topic_neural_networks", ...}

# 2. Ask a question
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "collection_name": "topic_neural_networks",
    "question": "What are the main architectures discussed?"
  }'

# 3. Get history
curl http://localhost:8000/api/history/list

# 4. Delete collection when done
curl -X DELETE http://localhost:8000/api/papers/collections/topic_neural_networks
```

---

## Support

For API support:
- Check interactive docs at `/docs`
- Review error messages
- Check logs for detailed errors
- Open an issue on GitHub

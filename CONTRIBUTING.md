# Contributing to Research Paper Assistant

Thank you for your interest in contributing to the Research Paper Assistant project!

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, Node version)

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and motivation
- Possible implementation approach
- Any relevant examples

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Development Guidelines

### Backend (Python)

**Code Style**
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

**Example:**
```python
async def process_document(doc_id: str) -> Dict[str, Any]:
    """
    Process a document and return results.
    
    Args:
        doc_id: Unique document identifier
        
    Returns:
        Dictionary containing processed results
    """
    # Implementation
    pass
```

**File Organization**
- Services in `backend/services/`
- Routes in `backend/api/routes/`
- Models in `backend/models/` (future)
- Utils in `backend/utils/` (future)

**Testing**
- Write unit tests for new functions
- Test error cases
- Use pytest

### Frontend (Angular)

**Code Style**
- Follow Angular style guide
- Use TypeScript strict mode
- Component-based architecture
- Reactive programming with RxJS

**Example:**
```typescript
export class MyComponent implements OnInit {
  data$: Observable<Data[]>;
  
  constructor(private service: DataService) {}
  
  ngOnInit(): void {
    this.data$ = this.service.getData();
  }
}
```

**Component Structure**
- One component per file
- Separate HTML, SCSS, and TS files
- Use OnPush change detection when possible
- Unsubscribe from observables

**Styling**
- Use SCSS
- Follow glassmorphism design patterns
- Maintain consistent spacing
- Ensure responsive design

## Project Structure Rules

### Backend Structure
```
backend/
├── api/
│   └── routes/          # API endpoints
├── services/            # Business logic
├── models/              # Data models (future)
├── utils/               # Helper functions (future)
└── tests/               # Test files (future)
```

### Frontend Structure
```
frontend/src/app/
├── components/          # UI components
├── services/            # Data services
├── models/              # TypeScript interfaces
└── shared/              # Shared components (future)
```

## Coding Standards

### Python

**Good:**
```python
async def search_papers(query: str, limit: int = 5) -> List[Paper]:
    """Search for papers matching the query."""
    results = await api_client.search(query, limit)
    return [Paper.from_dict(r) for r in results]
```

**Bad:**
```python
def search(q, l=5):  # No type hints, unclear names
    r = api.search(q, l)  # Not async
    return r
```

### TypeScript

**Good:**
```typescript
interface SearchRequest {
  topic: string;
  limit?: number;
  provider?: string;
}

searchPapers(request: SearchRequest): Observable<SearchResponse> {
  return this.http.post<SearchResponse>('/api/papers/search', request);
}
```

**Bad:**
```typescript
searchPapers(topic, limit, provider) {  // No types
  return this.http.post('/api/papers/search', {topic, limit, provider});
}
```

## Testing Guidelines

### Backend Tests
```python
import pytest
from services.pdf_processor import PDFProcessor

@pytest.mark.asyncio
async def test_pdf_download():
    processor = PDFProcessor()
    content = await processor.download_pdf("https://example.com/paper.pdf")
    assert content is not None
    assert len(content) > 0
```

### Frontend Tests
```typescript
describe('SearchComponent', () => {
  it('should validate topic input', () => {
    component.topic = '';
    component.onSearch();
    expect(component.error).toBeTruthy();
  });
});
```

## Documentation

### Code Documentation
- Write clear docstrings for Python functions
- Add JSDoc comments for TypeScript methods
- Explain complex logic with inline comments
- Update README when adding features

### API Documentation
- Document all endpoints in route files
- Include request/response examples
- Specify error codes and messages
- Use Pydantic models for validation

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Add comments to complex code
   - Update FEATURES.md for new features

2. **Test Your Changes**
   - Run existing tests
   - Add new tests
   - Test manually

3. **Check Code Quality**
   - Run linter (flake8 for Python, eslint for TypeScript)
   - Fix any warnings
   - Ensure consistent formatting

4. **Write Clear PR Description**
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Any breaking changes?

5. **Small, Focused PRs**
   - One feature per PR
   - Keep changes minimal
   - Easy to review and merge

## Areas for Contribution

### High Priority
- [ ] PostgreSQL integration
- [ ] User authentication
- [ ] Unit tests
- [ ] Error handling improvements
- [ ] Performance optimization

### Medium Priority
- [ ] Export functionality (PDF/Word)
- [ ] Advanced search filters
- [ ] Paper recommendations
- [ ] Citation visualization
- [ ] Batch processing

### Nice to Have
- [ ] Mobile app
- [ ] Browser extension
- [ ] Multi-language support
- [ ] Custom embedding models
- [ ] Collaborative features

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing private information

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for making this project better!

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.rag_pipeline import RAGPipeline

router = APIRouter()

class QueryRequest(BaseModel):
    collection_name: str
    question: str
    n_results: Optional[int] = 5
    mode: Optional[str] = "standard"  # standard, compare, literature_review, research_gaps
    provider: Optional[str] = "gemini"

class QueryResponse(BaseModel):
    success: bool
    answer: Optional[str] = None
    sources: Optional[list] = None
    sources_count: Optional[int] = None
    error: Optional[str] = None

@router.post("/query", response_model=QueryResponse)
async def query_papers(request: QueryRequest):
    """
    Ask a question about the indexed papers
    """
    try:
        pipeline = RAGPipeline(provider=request.provider)
        result = await pipeline.query(
            collection_name=request.collection_name,
            question=request.question,
            n_results=request.n_results,
            mode=request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_papers(request: QueryRequest):
    """
    Compare multiple papers on a specific aspect
    """
    request.mode = "compare"
    return await query_papers(request)

@router.post("/literature-review")
async def generate_literature_review(request: QueryRequest):
    """
    Generate a literature review based on indexed papers
    """
    request.mode = "literature_review"
    return await query_papers(request)

@router.post("/research-gaps")
async def identify_research_gaps(request: QueryRequest):
    """
    Identify research gaps in the indexed papers
    """
    request.mode = "research_gaps"
    return await query_papers(request)

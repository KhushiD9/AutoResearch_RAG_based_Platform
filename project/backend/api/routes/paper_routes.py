from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.rag_pipeline import RAGPipeline

router = APIRouter()

class SearchRequest(BaseModel):
    topic: str
    limit: Optional[int] = 5
    provider: Optional[str] = "gemini"

class SearchResponse(BaseModel):
    success: bool
    collection_name: Optional[str] = None
    papers_found: Optional[int] = None
    papers_processed: Optional[int] = None
    processed_papers: Optional[List[dict]] = None
    error: Optional[str] = None

@router.post("/search", response_model=SearchResponse)
async def search_and_index_papers(request: SearchRequest):
    """
    Search for papers on a given topic and index them in the vector database
    """
    try:
        pipeline = RAGPipeline(provider=request.provider)
        result = await pipeline.index_papers(request.topic, request.limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections")
async def list_collections():
    """
    List all available paper collections
    """
    try:
        from services.vector_store import VectorStore
        vector_store = VectorStore()
        collections = vector_store.list_collections()
        return {
            "success": True,
            "collections": collections,
            "count": len(collections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """
    Delete a paper collection
    """
    try:
        from services.vector_store import VectorStore
        vector_store = VectorStore()
        success = vector_store.delete_collection(collection_name)
        
        if success:
            return {
                "success": True,
                "message": f"Collection {collection_name} deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Collection not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

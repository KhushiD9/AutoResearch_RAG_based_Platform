from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# In-memory storage (replace with PostgreSQL in production)
history_storage = []

class HistoryEntry(BaseModel):
    id: Optional[str] = None
    collection_name: str
    question: str
    answer: str
    mode: str
    timestamp: Optional[datetime] = None

class HistoryResponse(BaseModel):
    success: bool
    entries: List[HistoryEntry]
    count: int

@router.post("/save")
async def save_history_entry(entry: HistoryEntry):
    """
    Save a query to history
    """
    try:
        entry.id = str(len(history_storage) + 1)
        entry.timestamp = datetime.now()
        history_storage.append(entry.dict())
        
        return {
            "success": True,
            "message": "History entry saved",
            "id": entry.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=HistoryResponse)
async def get_history(limit: Optional[int] = 50):
    """
    Get query history
    """
    try:
        entries = history_storage[-limit:] if len(history_storage) > limit else history_storage
        entries.reverse()
        
        return {
            "success": True,
            "entries": entries,
            "count": len(entries)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{entry_id}")
async def delete_history_entry(entry_id: str):
    """
    Delete a history entry
    """
    try:
        global history_storage
        history_storage = [entry for entry in history_storage if entry['id'] != entry_id]
        
        return {
            "success": True,
            "message": "History entry deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear")
async def clear_history():
    """
    Clear all history
    """
    try:
        global history_storage
        history_storage = []
        
        return {
            "success": True,
            "message": "History cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

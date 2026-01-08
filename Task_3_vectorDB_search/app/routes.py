from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.search import semantic_search

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 3


@router.post("/search")
def search(req: SearchRequest):
    try:
        results = semantic_search(req.query, req.top_k)
        return {
            "query": req.query,
            "results": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        
        raise HTTPException(status_code=500, detail="Internal server error")

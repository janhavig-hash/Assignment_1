from pydantic import BaseModel
from typing import List, Optional


class Citation(BaseModel):
    source: str
    page: Optional[int] = None
    text: str


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]

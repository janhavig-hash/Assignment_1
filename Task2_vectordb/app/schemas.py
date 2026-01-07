from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    query: str
    matched_document: str
    similarity: float
    query_embedding_preview: List[float]
    document_embedding_preview: List[float]

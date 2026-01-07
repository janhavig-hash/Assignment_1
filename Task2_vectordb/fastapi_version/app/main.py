from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import store_document, search

app = FastAPI()


@app.on_event("startup")
def startup():
    store_document()


class QueryRequest(BaseModel):
    query: str

@app.post("/search")
def query_docs(request: QueryRequest):
    return search(request.query)

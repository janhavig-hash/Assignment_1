from fastapi import APIRouter, HTTPException, status
import logging

from app.models.request import QueryRequest
from app.models.response import QueryResponse, Citation
from app.services.embedding import embed_query
from app.services.vector_store import collection 
from app.services.llm import generate_answer


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/query", response_model=QueryResponse)
def query_docs(request: QueryRequest):
    try:
        # 1. Input validation
        question = request.question.strip()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )

        # 2. Generate query embedding
        query_embedding = embed_query(question)

        #3. vector search
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=10,  
        )

        if (
            not results
            or "documents" not in results
            or not results["documents"]
            or not results["documents"][0]
        ):
            
            return QueryResponse(
                answer="I couldn't find any documents. Please upload a PDF first.",
                citations=[]
            )

        contexts = []
        citations = []
        seen_chunks = set()  

        # 4. Construct Context & Citations

        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            
            # Create a unique signature to prevent duplicates
            chunk_signature = f"{meta.get('page')}_{doc[:50]}"
            
            if chunk_signature in seen_chunks:
                continue  
            
            seen_chunks.add(chunk_signature)

            # Add to context for LLM
            contexts.append({
                "text": doc,
                "page": meta.get("page")
            })

            # Add to citations for the User Response
            citations.append(
                Citation(
                    source=meta.get("source", "uploaded_pdf"),
                    page=meta.get("page"),
                    text=doc[:300]  
                )
            )

        # 5. Fallback if context list is empty
        if not contexts:
            return QueryResponse(
                answer="The document does not contain information relevant to your question.",
                citations=[]
            )

        # 6. Generate answer using RAG
        answer = generate_answer(question, contexts)

        return QueryResponse(
            answer=answer,
            citations=citations
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"

        )

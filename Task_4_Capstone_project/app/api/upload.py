from fastapi import APIRouter, UploadFile, File, HTTPException, status
import logging
import shutil
from pathlib import Path

from app.core.config import UPLOAD_DIR, MAX_FILE_SIZE_MB
from app.services.pdf_service import extract_text_from_pdf
from app.services.embedding import embed_texts
from app.services.vector_store import store_chunks, collection

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # 1. Basic validation
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

        # 2. Size Validation 
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
             raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds {MAX_FILE_SIZE_MB} MB limit"
            )

        # 3. Save file temporarily
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"PDF uploaded: {file.filename}")

        # 4. Extract text & Chunk 
        chunks = extract_text_from_pdf(str(file_path))

        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No text could be extracted from the PDF"
            )

        # 5. Generate Embeddings
        
        text_list = [chunk["text"] for chunk in chunks]
        embeddings = embed_texts(text_list)

        if not embeddings or len(embeddings) != len(chunks):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Embedding generation failed"
            )

        # 6. Store in Vector DB
        store_chunks(chunks, embeddings)

        logger.info(f"Stored {len(chunks)} chunks from {file.filename}")

        
        return {
            "status": "success",  
            "message": "Document processed successfully",
            "chunks_stored": len(chunks),
            "filename": file.filename
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("PDF upload failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )


@router.delete("/reset")
def reset_database():
    try:
        # Check current count
        count = collection.count()
        if count == 0:
             return {"status": "success", "message": "Database is already empty."}

        # Delete everything
        collection.delete(where={}) 
        
        return {"status": "success", "message": f"Deleted {count} records. Database is clean."}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset database: {str(e)}"

        )

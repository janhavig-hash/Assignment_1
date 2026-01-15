from fastapi import FastAPI
from app.core.config import APP_NAME, APP_VERSION
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app = FastAPI(
    title = APP_NAME,
    version = APP_VERSION
)

#ROUTERS
app.include_router(upload_router, prefix = "/api")
app.include_router(query_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok", "message":"Tax Assitant API is running"}

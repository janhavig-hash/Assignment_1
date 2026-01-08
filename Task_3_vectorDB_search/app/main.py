from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Vector DB Demo API")

# Register routes
app.include_router(router)

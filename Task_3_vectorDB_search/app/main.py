from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Vector DB Demo API")


app.include_router(router)


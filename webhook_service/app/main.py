from fastapi import FastAPI
from app.entrypoints.webhook_handler import router as webhook_router
from app.adapters.orm import init_db

app = FastAPI()

init_db()

app.include_router(webhook_router)

@app.get("/")
def read_root():
    return {"message": "Webhook Service is running"}

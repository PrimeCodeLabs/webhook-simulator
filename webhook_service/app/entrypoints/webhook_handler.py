from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.adapters.database import SessionLocal
from app.core.services import create_order_event
from pydantic import BaseModel

router = APIRouter()

class OrderEventCreate(BaseModel):
    event_type: str
    order_id: int
    event_data: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/webhook")
def handle_webhook(event: OrderEventCreate, db: Session = Depends(get_db)):
    db_event = create_order_event(db, event.event_type, event.order_id, event.event_data)
    return db_event

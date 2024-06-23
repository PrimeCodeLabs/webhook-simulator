from sqlalchemy.orm import Session
from app.core.models import OrderEvent

def create_order_event(db: Session, event_type: str, order_id: int, event_data: str):
    db_event = OrderEvent(event_type=event_type, order_id=order_id, event_data=event_data)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

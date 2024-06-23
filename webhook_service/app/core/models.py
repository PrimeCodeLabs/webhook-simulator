from sqlalchemy import Column, Integer, String, DateTime
from app.adapters.database import Base
from datetime import datetime

class OrderEvent(Base):
    __tablename__ = "order_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True)
    order_id = Column(Integer, index=True)
    event_data = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

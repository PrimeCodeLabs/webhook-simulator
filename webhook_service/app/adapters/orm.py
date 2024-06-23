from .database import Base, engine
from app.core.models import OrderEvent

def init_db():
    Base.metadata.create_all(bind=engine)

Here's an updated version of the README with a focus on the webhook aspect:

---

# Webhook Implementation with Hexagonal Architecture, Docker, and FastAPI

This project demonstrates a webhook implementation using Hexagonal Architecture, FastAPI, Docker, and Docker Compose. It separates the core logic from infrastructure concerns, making the system more maintainable and scalable. The use of Docker ensures that the application can be easily deployed and managed in different environments.

## Project Overview

The project simulates a real-world e-commerce platform where order events (like order creation, update, and cancellation) are sent to a webhook endpoint. The webhook processes these events and stores them in a database for monitoring and analysis.

### Key Components

1. **FastAPI Server**: Manages the webhook endpoints and processes incoming events.
2. **Hexagonal Architecture**: Separates the core logic from infrastructure concerns, enhancing maintainability and scalability.
3. **Database**: Stores event data for analysis.
4. **Event Simulation App**: Simulates e-commerce order events and sends them to the webhook.
5. **Docker and Docker Compose**: Containerize the applications for easy deployment and management.

## Project Structure

```
webhook_project/
├── webhook_service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   └── orm.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── services.py
│   │   ├── entrypoints/
│   │   │   ├── __init__.py
│   │   │   └── webhook_handler.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── event_simulator/
│   ├── app/
│   │   ├── __init__.py
│   │   └── simulator.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── docker-compose.yml
└── README.md
```

## Running the Project

### Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

### Steps to Run

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PrimeCodeLabs/webhook-simulator.git
   cd webhook_project
   ```

2. **Build and run the containers**:

   ```bash
   docker-compose up --build
   ```

3. **Access the webhook service**:
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000). You should see a message indicating that the webhook service is running.

### Verifying the Setup

1. **Check Webhook Service Health**:

   ```bash
   curl http://localhost:8000
   ```

2. **Inspect Container Health Status**:
   ```bash
   docker inspect --format='{{json .State.Health}}' webhook_project-webhook_service-1 | jq
   ```

## Project Components

### Webhook Service

**Webhook Service**: Listens for incoming events and processes them using the core business logic defined in the Hexagonal Architecture.

- **Endpoints**:
  - `POST /webhook`: Receives and processes order events.

**app/main.py**:

```python
from fastapi import FastAPI
from app.entrypoints.webhook_handler import router as webhook_router
from app.adapters.orm import init_db

app = FastAPI()

init_db()

app.include_router(webhook_router)

@app.get("/")
def read_root():
    return {"message": "Webhook Service is running"}
```

**app/entrypoints/webhook_handler.py**:

```python
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
```

### Event Simulator

**Event Simulator**: Simulates e-commerce order events and sends them to the webhook endpoint.

**event_simulator/app/simulator.py**:

```python
import requests
import time
import random

webhook_url = "http://webhook_service:8000/webhook"

def simulate_event():
    event_types = ["order_created", "order_updated", "order_cancelled"]
    order_id = random.randint(1, 1000)
    event_type = random.choice(event_types)
    event_data = f"Order {order_id} {event_type}"

    payload = {
        "event_type": event_type,
        "order_id": order_id,
        "event_data": event_data
    }

    response = requests.post(webhook_url, json=payload)
    print(response.json())

if __name__ == "__main__":
    while True:
        simulate_event()
        time.sleep(5)
```

## Conclusion

This project showcases an advanced implementation of webhooks using FastAPI and Hexagonal Architecture, containerized with Docker. It provides a robust and scalable solution for processing and monitoring webhook events in a real-world scenario.

Feel free to explore and enhance the project further to suit your specific needs.

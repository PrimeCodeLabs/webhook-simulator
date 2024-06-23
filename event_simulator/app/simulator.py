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

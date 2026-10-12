
from fastapi import FastAPI

app = FastAPI(
    title="OmniSight API",
    description="API for OmniSight's automated UI testing agent",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OmniSight API",
    }


@app.post("/webhook")
def receive_webhook(payload: dict):
    return {
        "status": "received",
        "message": "Webhook received successfully",
    }

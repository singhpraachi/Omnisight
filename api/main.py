from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


class WebhookPayload(BaseModel):
    event: str
    repository: str
    build_id: str
    url: HttpUrl

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
def receive_webhook(payload: WebhookPayload):
    return {
        "status": "received",
        "message": "Webhook received successfully",
    }

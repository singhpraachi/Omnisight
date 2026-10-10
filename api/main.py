
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

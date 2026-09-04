from fastapi import FastAPI
from pydantic import BaseModel

from app.services.featherless import FeatherlessService


app = FastAPI(
    title="ShadowCode Security Agent",
    description="Autonomous DevSecOps security agent",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "ShadowCode Security Agent is running",
        "status": "online",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    service = FeatherlessService()

    response = await service.chat(
        request.message
    )

    return {
        "response": response
    }
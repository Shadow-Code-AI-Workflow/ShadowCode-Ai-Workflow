from fastapi import FastAPI

from app.schemas.models import (
    ChatRequest,
    CodeAnalysisRequest,
    SecurityAnalysis,
)

from app.services.featherless import FeatherlessService

app = FastAPI(
    title="ShadowCode Security Agent",
    description="Autonomous DevSecOps security agent",
    version="0.1.0",
)

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

@app.post("/analyze", response_model=SecurityAnalysis)
async def analyze_code(request: CodeAnalysisRequest):
    from app.services.security_agent import SecurityAgent

    agent = SecurityAgent()

    analysis = await agent.analyze_code(
        request.code
    )

    return {
        "analysis": analysis
    }
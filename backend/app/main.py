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

class CodeAnalysisRequest(BaseModel):
    code: str

class Vulnerability(BaseModel):
    name: str
    severity: str
    description: str
    evidence: str
    impact: str
    remediation: str
    confidence: str


class SecurityAnalysis(BaseModel):
    vulnerabilities: list[Vulnerability]

class AnalysisResponse(BaseModel):
    analysis: SecurityAnalysis

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

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest):
    from app.services.security_agent import SecurityAgent

    agent = SecurityAgent()

    analysis = await agent.analyze_code(
        request.code
    )

    return {
        "analysis": analysis
    }
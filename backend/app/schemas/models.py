from pydantic import BaseModel
from typing import List


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
    vulnerabilities: List[Vulnerability]
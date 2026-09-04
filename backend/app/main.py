from fastapi import FastAPI

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
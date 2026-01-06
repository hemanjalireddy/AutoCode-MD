from fastapi import FastAPI
from src.backend.api.v1.routes import router as v1_router

app = FastAPI(title="CuraLogic API", version="0.2.0")

# Include Routes
app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend"}
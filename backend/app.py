from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json
import os
from rag_engine import RAGEngine
from feedback_logger import FeedbackLogger

app = FastAPI(title="WiSo Chatbot API", version="1.0.0")

# CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Engine + Feedback Logger initialisieren
rag_engine = RAGEngine()
feedback_logger = FeedbackLogger()

class ChatRequest(BaseModel):
    message: str
    language: str = "de"

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: list = []

class FeedbackRequest(BaseModel):
    user_id: str
    query: str
    answer: str
    rating: int  # 1-5
    category: str = None

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        answer, confidence, sources = rag_engine.query(request.message, request.language)
        return ChatResponse(
            answer=answer,
            confidence=confidence,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def log_feedback(request: FeedbackRequest):
    try:
        feedback_logger.log(request.dict())
        return {"status": "logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        stats = feedback_logger.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

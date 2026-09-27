from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ai_service import ai_service
from schemas import (
    ExplanationRequest,
    LearningPathRequest,
    LearningPathResponse,
    QuestionRequest,
    QuizRequest,
    QuizResponse,
    SummaryRequest,
    TextResponse,
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini powered learning assistant.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/api/qa", response_model=TextResponse)
def qa(request: QuestionRequest):
    try:
        return {"result": ai_service.answer_question(request.question)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/explain", response_model=TextResponse)
def explain(request: ExplanationRequest):
    try:
        return {"result": ai_service.explain(request.topic)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/summarize", response_model=TextResponse)
def summarize(request: SummaryRequest):
    try:
        return {"result": ai_service.summarize(request.text)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/quiz", response_model=QuizResponse)
def quiz(request: QuizRequest):
    try:
        data = ai_service.quiz(request.topic)
        return {"topic": request.topic, "questions": data["questions"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/learning-path", response_model=LearningPathResponse)
def learning_path(request: LearningPathRequest):
    try:
        return {
            "goal": request.goal,
            "steps": ai_service.learning_path(request.goal),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

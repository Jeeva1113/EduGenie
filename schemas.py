from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=5000)


class ExplanationRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=5000)


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=5000)


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=20000)


class LearningPathRequest(BaseModel):
    goal: str = Field(..., min_length=2, max_length=5000)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    topic: str
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


class TextResponse(BaseModel):
    result: str


class LearningPathResponse(BaseModel):
    goal: str
    steps: list[str]

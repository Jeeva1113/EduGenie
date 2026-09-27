import pytest
from fastapi.testclient import TestClient
import main


class FakeAI:
    def answer_question(self, question):
        return f"Answer for: {question}"

    def explain(self, topic):
        return f"Explanation for: {topic}"

    def summarize(self, text):
        return "Short summary"

    def quiz(self, topic):
        return {
            "questions": [
                {
                    "question": f"Question {i}",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "A is correct.",
                }
                for i in range(1, 4)
            ]
        }

    def learning_path(self, goal):
        return ["Basics", "Practice", "Projects", "Revision", "Assessment"]


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "ai_service", FakeAI())
    return TestClient(main.app)

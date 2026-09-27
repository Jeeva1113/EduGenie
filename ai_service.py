import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv()


class AIService:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def _generate(self, prompt: str) -> str:
        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to the .env file."
            )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()

    def answer_question(self, question: str) -> str:
        prompt = f"""
You are EduGenie, a friendly learning assistant.
Answer the student's question accurately and clearly.
Use beginner-friendly language, short sections, and examples when useful.
Do not invent sources or facts.

Student question:
{question}
"""
        return self._generate(prompt)

    def explain(self, topic: str) -> str:
        prompt = f"""
You are EduGenie.
Explain the following topic to a beginner.
Use:
1. Simple definition
2. How it works
3. A real-world example
4. Three key points
Keep it concise.

Topic:
{topic}
"""
        return self._generate(prompt)

    def summarize(self, text: str) -> str:
        prompt = f"""
Summarize the following study material for a student.
Keep the important ideas, remove repetition, and use clear bullet points.
Do not add information that is not in the supplied text.

Text:
{text}
"""
        return self._generate(prompt)

    def quiz(self, topic: str) -> dict[str, Any]:
        prompt = f"""
Create exactly 3 multiple-choice questions for a student learning:
{topic}

Return ONLY valid JSON in this exact shape:
{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "answer": "the exact correct option text",
      "explanation": "short explanation"
    }}
  ]
}}

Rules:
- exactly 3 questions
- exactly 4 options per question
- one correct answer per question
- answer must exactly match one option
- no markdown
"""
        raw = self._generate(prompt)
        return self._parse_json(raw)

    def learning_path(self, goal: str) -> list[str]:
        prompt = f"""
Create a practical beginner-friendly learning path for this goal:
{goal}

Return ONLY valid JSON:
{{"steps": ["step 1", "step 2", "step 3", "step 4", "step 5", "step 6"]}}

Give 5 to 8 ordered steps. Keep each step short.
"""
        data = self._parse_json(self._generate(prompt))
        steps = data.get("steps")
        if not isinstance(steps, list) or not steps:
            raise RuntimeError("Gemini returned an invalid learning path.")
        return [str(step) for step in steps]

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            lines = [line for line in lines if not line.strip().startswith("```")]
            cleaned = "\n".join(lines).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Gemini returned invalid JSON.") from exc


ai_service = AIService()

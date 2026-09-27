# EduGenie – Google Gemini Powered Learning Assistant

Complete capstone project with FastAPI, Gemini AI, frontend, tests, and Docker.

## Windows setup

Open this folder in VS Code, then Terminal:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
```

Run:

```powershell
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

Run tests:

```powershell
pytest -q
```

## Features / Epic 2
- POST /api/qa
- POST /api/explain
- POST /api/quiz
- POST /api/summarize
- POST /api/learning-path

## Epic 4
- Local Uvicorn run
- Swagger/OpenAPI docs
- Automated pytest tests
- Docker support

## GitHub

Never commit `.env`.

```powershell
git init
git add .
git commit -m "Build EduGenie core functionality"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

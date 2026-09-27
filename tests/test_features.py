def test_qa(client):
    response = client.post("/api/qa", json={"question": "What is AI?"})
    assert response.status_code == 200
    assert "AI" in response.json()["result"]


def test_explain(client):
    response = client.post("/api/explain", json={"topic": "Neural networks"})
    assert response.status_code == 200
    assert response.json()["result"]


def test_quiz(client):
    response = client.post("/api/quiz", json={"topic": "Python"})
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) == 3
    assert all(len(q["options"]) == 4 for q in questions)


def test_summary(client):
    response = client.post(
        "/api/summarize",
        json={"text": "This is a long study paragraph with enough text to test the endpoint."},
    )
    assert response.status_code == 200
    assert response.json()["result"] == "Short summary"


def test_learning_path(client):
    response = client.post(
        "/api/learning-path",
        json={"goal": "Learn Python"},
    )
    assert response.status_code == 200
    assert len(response.json()["steps"]) == 5

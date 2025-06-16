from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is running!"}

def test_generate_response_endpoint():
    test_message = "Hello, AI!"
    test_chat_id = 12345
    response = client.post(
        "/api/v1/generate_response",
        json={
            "message": test_message,
            "chat_id": test_chat_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["chat_id"] == test_chat_id
    assert f"Вы сказали: \"{test_message}\". Я пока не могу генерировать ответы, но работаю над этим." in data["response"] 
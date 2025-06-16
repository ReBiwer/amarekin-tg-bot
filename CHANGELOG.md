# CHANGELOG

## 2024-05-27

- Initial project setup: Created directory structure, `README.md`, and `CHANGELOG.md`.

## 2025-06-09

- Configured `uv` and installed initial dependencies (`aiogram`, `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-jose`, `langchain`, `PyJWT`).
- Created `bot/main.py` with basic aiogram bot structure and integrated settings from `backend/app/core/config.py`.
- Created `backend/app/main.py` with basic FastAPI app and health check endpoint.
- Created `backend/app/core/config.py` for application settings using `pydantic_settings`.
- Informed user about manual `.env` file creation due to system limitations.
- Installed `httpx` for bot to backend communication.
- Updated `bot/main.py` to send messages to FastAPI backend and process responses.
- Created `backend/app/schemas/message.py` with Pydantic models for messages.
- Created `backend/app/api/v1/endpoints/ai.py` with AI response generation endpoint.
- Updated `backend/app/main.py` to include AI router.
- Installed `pytest` and created `tests/test_backend.py` for backend tests.
- Installed `langchain-openai`.
- Created `backend/app/services/ai_service.py` with Langchain integration.
- Updated `backend/app/api/v1/endpoints/ai.py` to use `AIService`.
- Updated `backend/app/core/config.py` to include `OPENAI_API_KEY`.
- Updated `backend/app/services/ai_service.py` to use `OPENAI_API_KEY` from settings.
- Updated `backend/app/main.py` to explicitly load environment variables from `.env`.
- Updated `backend/app/core/config.py` to include `DATABASE_URL`.
- Created `backend/app/db/database.py` for SQLAlchemy database setup.
- Created `backend/app/models/user.py` with SQLAlchemy User model.
- Created `backend/app/schemas/user.py` with Pydantic schemas for User.
- Created `backend/app/db/crud/user_crud.py` for user CRUD operations.
- Created `backend/app/api/v1/endpoints/users.py` with user API endpoints.
- Updated `backend/app/main.py` to include users router.
- Updated `bot/main.py` to handle user registration on `/start` command. 
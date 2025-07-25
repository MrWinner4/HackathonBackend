# BudgetBuddy Backend

## Overview
BudgetBuddy Backend is a RESTful API server built with **FastAPI** (Python) that powers the BudgetBuddy personal finance app. It manages users, goals, piggy banks, lessons, stories, and chatbot features, providing secure endpoints for all app data and logic.

## Features
- User authentication and management
- Goal creation, progress tracking, and deletion
- Piggy bank (balance) management
- Educational lessons and stories
- AI-powered chatbot endpoint
- CORS support for frontend integration

## Project Structure
```
app/
  main.py            # FastAPI app entrypoint
  routers/           # API route modules (users, goals, piggybank, etc.)
  models.py          # Database models
  ...
alembic/             # Database migrations
requirements.txt     # Python dependencies
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd HackathonBackend
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add required variables (see below).

## Environment Variables
The backend uses a `.env` file for configuration. Example:
```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
FIREBASE_CREDENTIALS=path/to/firebase.json
```

## Running the Server
Start the FastAPI server (default: http://127.0.0.1:8000):
```bash
uvicorn app.main:app --reload
```

## API Overview
- **Base URL:** `/`
- **Docs:** [Swagger UI](http://127.0.0.1:8000/docs)
- **Key Endpoints:**
  - `/users/` - User registration, login, profile
  - `/goals/` - CRUD for savings goals
  - `/piggy_bank/` - Balance management
  - `/lessons/` - Financial lessons
  - `/stories/` - Educational stories
  - `/chatbot/` - AI chatbot interface

## Dependencies
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [firebase-admin](https://pypi.org/project/firebase-admin/)
- See `requirements.txt` for full list

## Development Notes
- Use `alembic` for database migrations.
- All API changes should be documented in the OpenAPI schema (auto-generated by FastAPI).
- CORS is enabled for local frontend development.
- For production, review security and environment settings.

---

For questions or contributions, please open an issue or pull request. 
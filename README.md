# CodeSmith Consulting

A full-stack web application for CodeSmith Consulting LLC.

Contents
- backend/ — FastAPI backend with DynamoDB, JWT auth, service requests, bills, and mock payments
- frontend/ — React + Vite frontend

Quickstart
1. Backend
   - cd backend
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
   - cp .env.example .env and edit values (defaults target local DynamoDB at http://localhost:8000)
   - In another terminal (project root): docker compose up -d dynamodb
   - Run the API: uvicorn app.main:app --reload --port 8080 (on startup it will auto-create required DynamoDB tables if missing)
   - Optional: create tables manually with python backend/scripts/create_tables.py
2. Frontend
   - cd frontend
   - npm install
   - echo "VITE_API_BASE=http://localhost:8080" > .env
   - npm run dev

Security & Notes
- Passwords hashed with bcrypt; JWT access/refresh; CORS; basic security headers; rate limiting.
- Payments are mocked for demo; integrate Stripe for production.
- AWS DynamoDB required; see backend/README.md for details.


CodeSmith Consulting Backend (FastAPI)

Requirements
- Python 3.10+
- DynamoDB (AWS account or local dynamodb-local)

Setup
1. Create and activate a virtual environment.
2. pip install -r backend/requirements.txt
3. Copy backend/.env.example to backend/.env and adjust values (JWT_SECRET, etc.). For development, defaults point to local DynamoDB at http://localhost:8000 with dummy creds.
4. Tables: On startup, the API will auto-create these DynamoDB tables if they don't exist:
   - cs_users (PK: email [STRING])
   - cs_service_requests (PK: request_id [STRING])
   - cs_bills (PK: bill_id [STRING])
   - cs_payments (PK: payment_id [STRING])
   Optional: create GSI on cs_service_requests for user_id for efficient queries.
   Alternatively, you can run: python backend/scripts/create_tables.py
5. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8080 from backend/ directory.

Using DynamoDB Local (Docker)
- Start local instance: docker compose up -d dynamodb
- The backend (ENV=development) will automatically use http://localhost:8000.
- Stop: docker compose down

Admin setup
- Only the super admin can promote additional admins via POST /admin/users/promote (body: email string).
- All newly signed-up users are non-admin by default.

Security
- Passwords hashed with bcrypt (passlib).
- JWT access/refresh tokens.
- CORS restricted by ALLOWED_ORIGINS.
- Basic security headers + rate limiting (SlowAPI).

Endpoints (summary)
- POST /auth/signup {email, password, name, password_confirm, captcha_id, captcha_answer}
- POST /auth/login {email, password} -> tokens
- POST /auth/refresh (Authorization: Bearer <refresh>) -> new tokens
- GET /auth/me (auth) -> {user_id, email, name, is_admin}
- PUT /auth/profile (auth) {name?, first_name?, last_name?, phone?, address?, avatar_url?} -> update profile/contact info
- POST /auth/change-password (auth) {current_password, new_password}
- POST /auth/change-email (auth) {current_password, new_email} -> change login email
- GET /service-requests (auth)
- POST /service-requests (auth)
- GET /service-requests/{id} (auth)
- GET /bills (auth)
- GET /bills/{id} (auth)
- POST /bills/demo-create (auth) creates a sample unpaid bill
- POST /payments {bill_id, method} (auth) marks bill paid (mock)
- GET /admin/service-requests?user_id= (admin)
- GET /admin/bills?status=unpaid|paid&user_id= (admin)
- POST /admin/users/promote (super admin) — promote a user to admin by email

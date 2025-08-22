from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from .config import settings
from .routers import auth, service_requests, bills, payments
from .routers import contact as contact_router
from .routers import admin as admin_router
from .db import ensure_tables_if_not_exist

# Try to import SlowAPI (rate limiting). If unavailable, provide fallbacks so the app still runs.
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    from slowapi.middleware import SlowAPIMiddleware
    from slowapi.errors import RateLimitExceeded
    SLOWAPI_AVAILABLE = True
except Exception:  # ModuleNotFoundError or others
    SLOWAPI_AVAILABLE = False

    class Limiter:  # minimal shim
        def __init__(self, *args, **kwargs):
            pass

    def get_remote_address(request):  # simple fallback extractor
        client = request.client
        return client.host if client else "anonymous"

    class SlowAPIMiddleware:  # no-op middleware
        def __init__(self, app):
            self.app = app
        async def __call__(self, scope, receive, send):
            await self.app(scope, receive, send)

    class RateLimitExceeded(Exception):
        pass

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(title=settings.app_name)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limit middleware only if SlowAPI is available or use shim (safe either way)
app.add_middleware(SlowAPIMiddleware)

@app.on_event("startup")
async def startup_event():
    try:
        created = ensure_tables_if_not_exist()
        # Simple log to console; in production use a logger
        created_names = [k for k, v in created.items() if v]
        if created_names:
            print(f"Created DynamoDB tables: {', '.join(created_names)}")
        else:
            print("DynamoDB tables already exist.")
    except Exception as e:
        # Non-fatal: app will still start; endpoints will error if tables missing
        print(f"Warning: unable to ensure DynamoDB tables exist: {e}")
    # Ensure super admin exists
    try:
        from .routers.auth import ensure_super_admin
        created_sa = ensure_super_admin()
        if created_sa:
            print("Super admin user created.")
    except Exception as e:
        print(f"Warning: unable to ensure super admin exists: {e}")

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(service_requests.router)
app.include_router(bills.router)
app.include_router(payments.router)
app.include_router(contact_router.router)
app.include_router(admin_router.router)

# When SlowAPI is not installed, this handler will be effectively unused.
@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# For running locally:
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

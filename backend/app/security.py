from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _require_jwt():
    try:
        import jwt  # PyJWT provides the 'jwt' module
        return jwt
    except Exception as e:
        # Provide a clear, actionable message without crashing app import
        raise RuntimeError(
            "PyJWT is required for token operations but is not installed. "
            "Install dependencies with 'pip install -r backend/requirements.txt' or 'pip install PyJWT'."
        ) from e


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_token(subject: str, token_type: str = "access", expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = settings.access_token_expires if token_type == "access" else settings.refresh_token_expires
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "iss": settings.app_name,
    }
    jwt = _require_jwt()
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    jwt = _require_jwt()
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

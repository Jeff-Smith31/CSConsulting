from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timezone
import uuid, secrets, time, random
from ..schemas import SignupRequest, LoginRequest, TokenResponse, Message, ProfileUpdate, ChangePasswordRequest, ChangeEmailRequest
from ..security import hash_password, verify_password, create_token, decode_token
from ..db import get_table

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

USERS_TABLE = "cs_users"

# Super admin configuration (per requirements)
SUPER_ADMIN_EMAIL = "jeffrey.russell.smith@gmail.com"
SUPER_ADMIN_PASSWORD = "n2nj6Pqwe!"

# Simple in-memory captcha store: {captcha_id: (answer, expires_at)}
_CAPTCHAS: dict[str, tuple[int, float]] = {}
_CAPTCHA_TTL_SECONDS = 600


def _cleanup_captchas():
    now = time.time()
    expired = [k for k, (_, exp) in _CAPTCHAS.items() if exp < now]
    for k in expired:
        _CAPTCHAS.pop(k, None)


def get_current_user_id(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def _is_admin_user(user_id: str) -> bool:
    users = get_table(USERS_TABLE)
    # Users table PK is email; scan to find by user_id
    resp = users.scan()
    items = resp.get("Items", [])
    for it in items:
        if it.get("user_id") == user_id:
            email = it.get("email", "")
            role = it.get("role")
            if email.lower() == SUPER_ADMIN_EMAIL.lower():
                return True
            if role == "admin":
                return True
    return False


def require_admin(authorization: Optional[str] = Header(default=None)) -> str:
    user_id = get_current_user_id(authorization)
    if not _is_admin_user(user_id):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user_id


def require_super_admin(authorization: Optional[str] = Header(default=None)) -> str:
    user_id = get_current_user_id(authorization)
    users = get_table(USERS_TABLE)
    resp = users.scan()
    items = resp.get("Items", [])
    for it in items:
        if it.get("user_id") == user_id:
            if it.get("email", "").lower() == SUPER_ADMIN_EMAIL.lower():
                return user_id
    raise HTTPException(status_code=403, detail="Super admin privileges required")


def ensure_super_admin():
    """Ensure the super admin user exists with the specified email and password.
    Does not overwrite if already present.
    """
    users = get_table(USERS_TABLE)
    res = users.get_item(Key={"email": SUPER_ADMIN_EMAIL})
    if "Item" in res:
        return False
    user_id = str(uuid.uuid4())
    item = {
        "email": SUPER_ADMIN_EMAIL,
        "user_id": user_id,
        "name": "Super Admin",
        "password_hash": hash_password(SUPER_ADMIN_PASSWORD),
        "role": "admin",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    users.put_item(Item=item)
    return True


@router.get("/captcha")
def get_captcha():
    _cleanup_captchas()
    a, b = random.randint(1, 9), random.randint(1, 9)
    answer = a + b
    captcha_id = secrets.token_urlsafe(16)
    _CAPTCHAS[captcha_id] = (answer, time.time() + _CAPTCHA_TTL_SECONDS)
    return {"captcha_id": captcha_id, "question": f"What is {a} + {b}?"}


@router.post("/signup", response_model=Message)
def signup(body: SignupRequest):
    # Password confirmation check
    if body.password != body.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Captcha verification
    tup = _CAPTCHAS.pop(body.captcha_id, None)
    if not tup or tup[1] < time.time():
        raise HTTPException(status_code=400, detail="Captcha expired. Please try again.")
    expected = tup[0]
    try:
        provided = int(body.captcha_answer.strip())
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid captcha answer")
    if provided != expected:
        raise HTTPException(status_code=400, detail="Incorrect captcha answer")

    users = get_table(USERS_TABLE)
    # check if user exists
    res = users.get_item(Key={"email": body.email})
    if "Item" in res:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    item = {
        "email": body.email,
        "user_id": user_id,
        "name": body.name,
        "password_hash": hash_password(body.password),
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    users.put_item(Item=item)
    return {"message": "Account created. You can now log in."}


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    users = get_table(USERS_TABLE)
    res = users.get_item(Key={"email": body.email})
    item = res.get("Item")
    if not item or not verify_password(body.password, item.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_token(subject=item["user_id"], token_type="access")
    refresh = create_token(subject=item["user_id"], token_type="refresh")
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(authorization: Optional[str] = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload["sub"]
        access = create_token(subject=user_id, token_type="access")
        refresh = create_token(subject=user_id, token_type="refresh")
        return TokenResponse(access_token=access, refresh_token=refresh)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/me")
def me(authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    users = get_table(USERS_TABLE)
    resp = users.scan()
    items = resp.get("Items", [])
    for it in items:
        if it.get("user_id") == user_id:
            email = it.get("email")
            name = it.get("name")
            role = it.get("role")
            is_admin = (email and email.lower() == SUPER_ADMIN_EMAIL.lower()) or role == "admin"
            return {
                "user_id": user_id,
                "email": email,
                "name": name,
                "is_admin": bool(is_admin),
                "first_name": it.get("first_name"),
                "last_name": it.get("last_name"),
                "phone": it.get("phone"),
                "address": it.get("address"),
                "avatar_url": it.get("avatar_url"),
            }
    # If not found, return minimal info
    return {"user_id": user_id, "email": None, "name": None, "is_admin": False}


@router.put("/profile", response_model=Message)
def update_profile(body: ProfileUpdate, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    users = get_table(USERS_TABLE)
    resp = users.scan()
    items = resp.get("Items", [])
    for it in items:
        if it.get("user_id") == user_id:
            # Update provided fields only
            if body.first_name is not None:
                it["first_name"] = body.first_name
            if body.last_name is not None:
                it["last_name"] = body.last_name
            if body.phone is not None:
                it["phone"] = body.phone
            if body.address is not None:
                it["address"] = body.address
            if body.avatar_url is not None:
                it["avatar_url"] = body.avatar_url
            if body.name is not None:
                it["name"] = body.name
            else:
                # derive display name if first/last provided and name not explicitly set
                fn = it.get("first_name")
                ln = it.get("last_name")
                if fn or ln:
                    it["name"] = (f"{fn or ''} {ln or ''}").strip()
            users.put_item(Item=it)
            return {"message": "Profile updated"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/change-password", response_model=Message)
def change_password(body: ChangePasswordRequest, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    users = get_table(USERS_TABLE)
    resp = users.scan()
    items = resp.get("Items", [])
    for it in items:
        if it.get("user_id") == user_id:
            if not verify_password(body.current_password, it.get("password_hash", "")):
                raise HTTPException(status_code=400, detail="Current password is incorrect")
            it["password_hash"] = hash_password(body.new_password)
            users.put_item(Item=it)
            return {"message": "Password changed"}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/change-email", response_model=Message)
def change_email(body: ChangeEmailRequest, authorization: Optional[str] = Header(default=None)):
    """Change the user's email (PK). Verifies current password, ensures uniqueness,
    copies the item to the new PK while retaining user_id and role, then deletes the old item.
    Note: Super admin email cannot be changed for safety.
    """
    user_id = get_current_user_id(authorization)
    users = get_table(USERS_TABLE)

    # First, locate current item by user_id via scan
    resp = users.scan()
    items = resp.get("Items", [])
    current = None
    for it in items:
        if it.get("user_id") == user_id:
            current = it
            break
    if not current:
        raise HTTPException(status_code=404, detail="User not found")

    if current.get("email", "").lower() == SUPER_ADMIN_EMAIL.lower():
        raise HTTPException(status_code=400, detail="Super admin email cannot be changed")

    if not verify_password(body.current_password, current.get("password_hash", "")):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Ensure target email is free
    existing = users.get_item(Key={"email": str(body.new_email)})
    if "Item" in existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    # Create new item with same attributes but new PK
    new_item = dict(current)
    new_item["email"] = str(body.new_email)
    users.put_item(Item=new_item)
    # Delete old
    users.delete_item(Key={"email": current["email"]})

    return {"message": "Email updated"}

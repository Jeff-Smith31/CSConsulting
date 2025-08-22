from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)
    name: str
    captcha_id: str
    captcha_answer: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class User(BaseModel):
    user_id: str
    email: EmailStr
    name: str
    created_at: datetime

class ProfileUpdate(BaseModel):
    # Allow updating display and contact fields; all optional to support partial updates
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

class ServiceRequestCreate(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high"] = "medium"

class ServiceRequest(ServiceRequestCreate):
    request_id: str
    user_id: str
    status: Literal["open", "in_progress", "completed", "closed"] = "open"
    created_at: datetime

class Bill(BaseModel):
    bill_id: str
    user_id: str
    amount_cents: int
    description: str
    status: Literal["unpaid", "paid"] = "unpaid"
    due_date: datetime
    created_at: datetime

class PaymentRequest(BaseModel):
    bill_id: str
    method: Literal["card", "ach", "other"] = "card"

class Payment(BaseModel):
    payment_id: str
    bill_id: str
    user_id: str
    amount_cents: int
    method: str
    status: Literal["succeeded", "failed"]
    created_at: datetime

class Message(BaseModel):
    message: str

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

class PaginatedServiceRequests(BaseModel):
    items: List[ServiceRequest]
    last_evaluated_key: Optional[str] = None

class ChangeEmailRequest(BaseModel):
    current_password: str
    new_email: EmailStr

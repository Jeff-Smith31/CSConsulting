from fastapi import APIRouter
from ..schemas import ContactRequest, Message

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("", response_model=Message)
def submit_contact(body: ContactRequest):
    # In a real app, send an email or persist to DB. For now, log and return success.
    try:
        print(f"Contact message from {body.name} <{body.email}>: {body.message}")
    except Exception:
        pass
    return {"message": "Thanks! We received your message and will get back to you soon."}

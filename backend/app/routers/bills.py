from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime, timezone
import uuid
from ..schemas import Bill
from ..db import get_table
from .auth import get_current_user_id

router = APIRouter(prefix="/bills", tags=["bills"])

TABLE = "cs_bills"

@router.get("", response_model=list[Bill])
def list_bills(authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    resp = table.scan()
    items = [i for i in resp.get("Items", []) if i.get("user_id") == user_id]
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items

@router.get("/{bill_id}", response_model=Bill)
def get_bill(bill_id: str, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    resp = table.get_item(Key={"bill_id": bill_id})
    item = resp.get("Item")
    if not item or item.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Not found")
    return item

# Utility to create a demo bill for testing (would be internal/admin in production)
@router.post("/demo-create", response_model=Bill)
def create_demo_bill(authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    bill_id = str(uuid.uuid4())
    item = {
        "bill_id": bill_id,
        "user_id": user_id,
        "amount_cents": 25000,
        "description": "Consulting services",
        "status": "unpaid",
        "due_date": datetime.now(tz=timezone.utc).isoformat(),
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item

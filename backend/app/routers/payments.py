from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime, timezone
import uuid
from ..schemas import PaymentRequest, Payment, Message
from ..db import get_table
from .auth import get_current_user_id

router = APIRouter(prefix="/payments", tags=["payments"])

BILLS_TABLE = "cs_bills"
PAYMENTS_TABLE = "cs_payments"

@router.post("", response_model=Payment)
def pay_bill(body: PaymentRequest, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    bills = get_table(BILLS_TABLE)
    payments = get_table(PAYMENTS_TABLE)
    bill_resp = bills.get_item(Key={"bill_id": body.bill_id})
    bill = bill_resp.get("Item")
    if not bill or bill.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Bill not found")
    if bill.get("status") == "paid":
        raise HTTPException(status_code=400, detail="Bill already paid")

    # Mock payment success
    payment_id = str(uuid.uuid4())
    payment = {
        "payment_id": payment_id,
        "bill_id": body.bill_id,
        "user_id": user_id,
        "amount_cents": bill["amount_cents"],
        "method": body.method,
        "status": "succeeded",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    payments.put_item(Item=payment)

    bill["status"] = "paid"
    bills.put_item(Item=bill)

    return payment

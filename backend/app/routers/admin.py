from fastapi import APIRouter, Query, Header
from typing import Optional, List
from ..db import get_table
from .auth import require_admin, require_super_admin

router = APIRouter(prefix="/admin", tags=["admin"])

REQ_TABLE = "cs_service_requests"
BILLS_TABLE = "cs_bills"


@router.get("/service-requests")
def list_all_requests(user_id: Optional[str] = Query(default=None), authorization: Optional[str] = Header(default=None)):
    # Ensure caller is admin
    require_admin(authorization)
    table = get_table(REQ_TABLE)
    resp = table.scan()
    items = resp.get("Items", [])
    if user_id:
        items = [i for i in items if i.get("user_id") == user_id]
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


@router.get("/bills")
def list_bills_admin(
    status: Optional[str] = Query(default="unpaid"),
    user_id: Optional[str] = Query(default=None),
    authorization: Optional[str] = Header(default=None),
):
    require_admin(authorization)
    table = get_table(BILLS_TABLE)
    resp = table.scan()
    items = resp.get("Items", [])
    if status:
        items = [i for i in items if i.get("status") == status]
    if user_id:
        items = [i for i in items if i.get("user_id") == user_id]
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


@router.post("/users/promote")
def promote_user(email: str, authorization: Optional[str] = Header(default=None)):
    """Promote a user to admin by email. Only super admin may call this."""
    require_super_admin(authorization)
    users = get_table("cs_users")
    res = users.get_item(Key={"email": email})
    if "Item" not in res:
        return {"message": "User not found"}
    item = res["Item"]
    item["role"] = "admin"
    users.put_item(Item=item)
    return {"message": f"{email} promoted to admin"}

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime, timezone
import uuid
from ..schemas import ServiceRequestCreate, ServiceRequest, PaginatedServiceRequests
from ..db import get_table
from .auth import get_current_user_id

router = APIRouter(prefix="/service-requests", tags=["service_requests"])

TABLE = "cs_service_requests"

@router.post("", response_model=ServiceRequest)
def create_request(body: ServiceRequestCreate, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    request_id = str(uuid.uuid4())
    item = {
        "request_id": request_id,
        "user_id": user_id,
        "title": body.title,
        "description": body.description,
        "priority": body.priority,
        "status": "open",
        "created_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return ServiceRequest(**item)


@router.get("", response_model=list[ServiceRequest])
def list_requests(authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    # Using a scan with FilterExpression for simplicity. In production, use GSI on user_id.
    resp = table.scan()
    items = [i for i in resp.get("Items", []) if i.get("user_id") == user_id]
    # sort by created_at desc
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items


@router.get("/{request_id}", response_model=ServiceRequest)
def get_request(request_id: str, authorization: Optional[str] = Header(default=None)):
    user_id = get_current_user_id(authorization)
    table = get_table(TABLE)
    resp = table.get_item(Key={"request_id": request_id})
    item = resp.get("Item")
    if not item or item.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Not found")
    return item

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.flow_service import FlowService

router = APIRouter()

@router.get("/traffic")
def list_traffic_flows(
    protocol: Optional[str] = None,
    prediction: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    flows, total = FlowService.get_flows(
        db=db,
        protocol=protocol,
        prediction=prediction,
        search=search,
        page=page,
        limit=limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "items": [f.to_dict() for f in flows]
    }

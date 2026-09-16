from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.alert_service import AlertService
from app.schemas.alert import AlertUpdateStatus, AlertResponse

router = APIRouter()

@router.get("/alerts")
def list_alerts(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    attack_type: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    alerts, total = AlertService.get_alerts(
        db=db,
        severity=severity,
        status=status,
        attack_type=attack_type,
        search=search,
        page=page,
        limit=limit
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if total > 0 else 1,
        "items": [a.to_dict() for a in alerts]
    }

@router.get("/alerts/{alert_id}")
def get_alert_detail(alert_id: int, db: Session = Depends(get_db)):
    alert = AlertService.get_alert_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found.")
    return alert.to_dict()

@router.post("/alerts/{alert_id}/status")
def update_alert_status(alert_id: int, body: AlertUpdateStatus, db: Session = Depends(get_db)):
    valid_statuses = ["New", "Investigating", "Resolved", "False Positive"]
    if body.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status '{body.status}'. Must be one of {valid_statuses}"
        )

    updated_alert = AlertService.update_alert_status(db, alert_id, body.status)
    if not updated_alert:
        raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found.")

    return updated_alert.to_dict()

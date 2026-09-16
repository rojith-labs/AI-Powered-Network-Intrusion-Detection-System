from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.ml.predictor import predictor
from app.config import settings

router = APIRouter()

@router.get("/health")
def get_health(db: Session = Depends(get_db)):
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    ml_status = predictor.get_metadata()

    return {
        "status": "online",
        "version": settings.VERSION,
        "database": db_status,
        "model_loaded": predictor.is_loaded,
        "active_model": ml_status.get("model_name", "None"),
        "environment": settings.ENVIRONMENT
    }

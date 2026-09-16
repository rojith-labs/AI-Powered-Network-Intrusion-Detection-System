from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.ml.predictor import predictor
from app.ml.explainer import NIDSExplainer
from app.models.prediction import Prediction as PredictionModel
from app.services.alert_service import AlertService
from app.services.flow_service import FlowService

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_single_flow(req: PredictionRequest, db: Session = Depends(get_db)):
    features_dict = req.model_dump()

    # Model inference & threat scoring
    prediction, confidence, threat_score, severity, importances = predictor.predict_flow(features_dict)

    # Human-readable explanation
    explanation = NIDSExplainer.generate_explanation(prediction, confidence, features_dict)

    model_metadata = predictor.get_metadata()
    model_used = model_metadata.get("model_name", "AI-NIDS Classifier")

    # Persist prediction in DB
    db_pred = PredictionModel(
        model_name=model_used,
        prediction=prediction,
        confidence=confidence,
        threat_score=threat_score,
        features=json.dumps(features_dict)
    )
    db.add(db_pred)

    # Persist Flow in DB
    FlowService.create_flow(
        db=db,
        source_ip=req.source_ip or "192.168.1.100",
        destination_ip=req.destination_ip or "10.0.0.1",
        protocol="TCP" if req.protocol == 6 else ("UDP" if req.protocol == 17 else "ICMP"),
        source_port=req.source_port,
        destination_port=req.destination_port,
        duration=req.flow_duration,
        packet_count=req.fwd_pkts_count + req.bwd_pkts_count,
        byte_count=req.total_bytes,
        prediction=prediction,
        threat_score=threat_score
    )

    # If malicious and high threat, auto-create alert
    if threat_score > 20.0 and prediction not in ["BENIGN", "Normal"]:
        AlertService.create_alert(
            db=db,
            source_ip=req.source_ip or "192.168.1.100",
            destination_ip=req.destination_ip or "10.0.0.1",
            protocol="TCP" if req.protocol == 6 else ("UDP" if req.protocol == 17 else "ICMP"),
            source_port=req.source_port,
            destination_port=req.destination_port,
            attack_type=prediction,
            confidence=confidence,
            threat_score=threat_score,
            severity=severity,
            status="New"
        )

    db.commit()

    return {
        "prediction": prediction,
        "confidence": confidence,
        "threat_score": threat_score,
        "severity": severity,
        "explanation": explanation,
        "feature_importance": importances,
        "model_used": model_used
    }

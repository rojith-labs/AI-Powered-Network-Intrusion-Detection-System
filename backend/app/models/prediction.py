from datetime import datetime
import json
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    model_name = Column(String(50), nullable=False)
    prediction = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    threat_score = Column(Float, nullable=False)
    features = Column(Text, nullable=False)  # JSON string of features dictionary

    def get_features_dict(self):
        try:
            return json.loads(self.features)
        except Exception:
            return {}

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "model_name": self.model_name,
            "prediction": self.prediction,
            "confidence": round(self.confidence, 4),
            "threat_score": round(self.threat_score, 1),
            "features": self.get_features_dict()
        }

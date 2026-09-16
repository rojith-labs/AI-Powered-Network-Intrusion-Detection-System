from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(50), nullable=False, unique=True)
    version = Column(String(20), default="1.0.0")
    dataset_name = Column(String(50), nullable=False)
    trained_at = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    status = Column(String(20), default="Active") # Active, Deprecated, Training
    confusion_matrix = Column(Text, nullable=True) # JSON matrix

    def to_dict(self):
        import json
        cm = None
        if self.confusion_matrix:
            try:
                cm = json.loads(self.confusion_matrix)
            except Exception:
                cm = None
        return {
            "id": self.id,
            "model_name": self.model_name,
            "version": self.version,
            "dataset_name": self.dataset_name,
            "trained_at": self.trained_at.isoformat() if self.trained_at else None,
            "accuracy": round(self.accuracy, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
            "status": self.status,
            "confusion_matrix": cm
        }

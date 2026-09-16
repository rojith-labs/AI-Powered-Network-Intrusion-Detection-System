from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source_ip = Column(String(45), nullable=False, index=True)
    destination_ip = Column(String(45), nullable=False, index=True)
    protocol = Column(String(10), nullable=False, index=True)
    source_port = Column(Integer, nullable=False)
    destination_port = Column(Integer, nullable=False, index=True)
    attack_type = Column(String(50), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    threat_score = Column(Float, nullable=False)
    severity = Column(String(20), nullable=False, index=True)  # Normal, Low, Medium, High, Critical
    status = Column(String(30), default="New", index=True)     # New, Investigating, Resolved, False Positive

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "source_port": self.source_port,
            "destination_port": self.destination_port,
            "attack_type": self.attack_type,
            "confidence": round(self.confidence, 4),
            "threat_score": round(self.threat_score, 1),
            "severity": self.severity,
            "status": self.status
        }

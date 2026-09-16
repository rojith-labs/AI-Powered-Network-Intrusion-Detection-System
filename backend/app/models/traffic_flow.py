from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class TrafficFlow(Base):
    __tablename__ = "traffic_flows"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source_ip = Column(String(45), nullable=False, index=True)
    destination_ip = Column(String(45), nullable=False, index=True)
    protocol = Column(String(10), nullable=False, index=True)
    source_port = Column(Integer, nullable=False)
    destination_port = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)       # seconds
    packet_count = Column(Integer, nullable=False)
    byte_count = Column(Integer, nullable=False)
    prediction = Column(String(50), default="BENIGN", index=True)
    threat_score = Column(Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_ip": self.source_ip,
            "destination_ip": self.destination_ip,
            "protocol": self.protocol,
            "source_port": self.source_port,
            "destination_port": self.destination_port,
            "duration": round(self.duration, 4),
            "packet_count": self.packet_count,
            "byte_count": self.byte_count,
            "prediction": self.prediction,
            "threat_score": round(self.threat_score, 1)
        }

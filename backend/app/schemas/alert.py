from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AlertBase(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int
    destination_port: int
    attack_type: str
    confidence: float
    threat_score: float
    severity: str
    status: str = "New"

class AlertCreate(AlertBase):
    pass

class AlertUpdateStatus(BaseModel):
    status: str # New, Investigating, Resolved, False Positive

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertFilter(BaseModel):
    severity: Optional[str] = None
    status: Optional[str] = None
    attack_type: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 50

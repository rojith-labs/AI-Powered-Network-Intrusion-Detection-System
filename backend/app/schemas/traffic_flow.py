from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class TrafficFlowSchema(BaseModel):
    id: int
    timestamp: datetime
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int
    destination_port: int
    duration: float
    packet_count: int
    byte_count: int
    prediction: str
    threat_score: float

    class Config:
        from_attributes = True

class FlowFilter(BaseModel):
    protocol: Optional[str] = None
    prediction: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    limit: int = 50

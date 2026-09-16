from typing import List, Dict, Any
from pydantic import BaseModel

class PcapFlowItem(BaseModel):
    timestamp: str
    source_ip: str
    destination_ip: str
    protocol: str
    source_port: int
    destination_port: int
    duration: float
    packet_count: int
    byte_count: int
    prediction: str
    confidence: float
    threat_score: float
    severity: str
    explanation: List[str]

class PcapAnalysisResponse(BaseModel):
    filename: str
    file_size_bytes: int
    processed_at: str
    total_packets: int
    total_flows: int
    normal_flows: int
    suspicious_flows: int
    overall_threat_score: float
    overall_severity: str
    attack_categories: Dict[str, int]
    protocol_distribution: Dict[str, int]
    severity_distribution: Dict[str, int]
    alerts_generated: int
    flows: List[PcapFlowItem]

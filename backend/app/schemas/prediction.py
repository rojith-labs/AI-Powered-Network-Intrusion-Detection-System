from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class FeatureAttribution(BaseModel):
    feature: str
    value: float
    importance: float
    description: str

class PredictionRequest(BaseModel):
    flow_duration: float = Field(..., description="Flow duration in seconds")
    fwd_pkts_count: int = Field(..., description="Forward packet count")
    bwd_pkts_count: int = Field(..., description="Backward packet count")
    total_bytes: int = Field(..., description="Total bytes transferred")
    packet_rate: float = Field(0.0, description="Packets per second")
    bytes_per_sec: float = Field(0.0, description="Bytes per second")
    avg_pkt_size: float = Field(0.0, description="Average packet size in bytes")
    min_pkt_size: float = Field(0.0, description="Minimum packet size")
    max_pkt_size: float = Field(0.0, description="Maximum packet size")
    std_pkt_size: float = Field(0.0, description="Standard deviation of packet size")
    fwd_pkt_len_mean: float = Field(0.0, description="Mean forward packet length")
    fwd_pkt_len_std: float = Field(0.0, description="Std dev forward packet length")
    bwd_pkt_len_mean: float = Field(0.0, description="Mean backward packet length")
    bwd_pkt_len_std: float = Field(0.0, description="Std dev backward packet length")
    syn_flag_cnt: int = Field(0, description="SYN flag count")
    ack_flag_cnt: int = Field(0, description="ACK flag count")
    fin_flag_cnt: int = Field(0, description="FIN flag count")
    rst_flag_cnt: int = Field(0, description="RST flag count")
    psh_flag_cnt: int = Field(0, description="PSH flag count")
    source_port: int = Field(80, description="Source port")
    destination_port: int = Field(443, description="Destination port")
    protocol: int = Field(6, description="Protocol number (6=TCP, 17=UDP, 1=ICMP)")
    flow_iat_mean: float = Field(0.0, description="Mean inter-arrival time")
    flow_iat_std: float = Field(0.0, description="Std dev inter-arrival time")
    
    # Optional metadata
    source_ip: Optional[str] = "192.168.1.100"
    destination_ip: Optional[str] = "10.0.0.1"

class PredictionResponse(BaseModel):
    prediction: str                    # BENIGN, DoS, DDoS, Port Scan, Brute Force, Botnet, Web Attack, Infiltration, Other
    confidence: float                 # 0.0 to 1.0
    threat_score: float               # 0 to 100
    severity: str                     # Normal, Low, Medium, High, Critical
    explanation: List[str]            # Top human-readable indicators
    feature_importance: List[FeatureAttribution]
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

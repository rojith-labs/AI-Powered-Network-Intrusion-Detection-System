from typing import List, Dict, Any
from pydantic import BaseModel

class DashboardSummaryCards(BaseModel):
    total_traffic_bytes: int
    total_flows: int
    normal_traffic_count: int
    malicious_traffic_count: int
    critical_alerts_count: int
    active_threat_level: str

class TimeSeriesPoint(BaseModel):
    timestamp: str
    total_flows: int
    normal_flows: int
    malicious_flows: int

class NameCountPair(BaseModel):
    name: str
    count: int

class DashboardMetrics(BaseModel):
    summary: DashboardSummaryCards
    traffic_timeline: List[TimeSeriesPoint]
    attack_distribution: List[NameCountPair]
    severity_distribution: List[NameCountPair]
    protocol_distribution: List[NameCountPair]
    top_source_ips: List[NameCountPair]
    top_dest_ports: List[NameCountPair]
    recent_alerts: List[Dict[str, Any]]

class AnalyticsData(BaseModel):
    attack_frequency: List[NameCountPair]
    severity_trends: List[TimeSeriesPoint]
    traffic_volume_bytes: List[Dict[str, Any]]
    confidence_histogram: List[NameCountPair]
    protocol_distribution: List[NameCountPair]
    top_source_ips: List[NameCountPair]
    top_dest_ports: List[NameCountPair]

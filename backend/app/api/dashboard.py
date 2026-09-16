from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models.alert import Alert
from app.models.traffic_flow import TrafficFlow

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    # Total Flows
    total_flows = db.query(TrafficFlow).count()

    # Total Bytes & Traffic
    total_bytes_res = db.query(func.sum(TrafficFlow.byte_count)).scalar() or 0

    # Normal vs Malicious Traffic
    normal_count = db.query(TrafficFlow).filter(TrafficFlow.prediction.in_(["BENIGN", "Normal"])).count()
    malicious_count = total_flows - normal_count

    # Critical Alerts Count
    critical_alerts = db.query(Alert).filter(Alert.severity == "Critical").count()

    # Active Threat Level
    if critical_alerts > 5:
        threat_level = "CRITICAL"
    elif critical_alerts > 0 or (malicious_count > total_flows * 0.3):
        threat_level = "HIGH"
    elif malicious_count > 0:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    # Attack Distribution
    attack_counts = (
        db.query(Alert.attack_type, func.count(Alert.id))
        .group_by(Alert.attack_type)
        .all()
    )
    attack_dist = [{"name": name, "count": count} for name, count in attack_counts]

    # Severity Distribution
    sev_counts = (
        db.query(Alert.severity, func.count(Alert.id))
        .group_by(Alert.severity)
        .all()
    )
    severity_dist = [{"name": name, "count": count} for name, count in sev_counts]

    # Protocol Distribution
    proto_counts = (
        db.query(TrafficFlow.protocol, func.count(TrafficFlow.id))
        .group_by(TrafficFlow.protocol)
        .all()
    )
    protocol_dist = [{"name": name, "count": count} for name, count in proto_counts]

    # Top Source IPs
    top_ips = (
        db.query(TrafficFlow.source_ip, func.count(TrafficFlow.id).label("cnt"))
        .group_by(TrafficFlow.source_ip)
        .order_by(desc("cnt"))
        .limit(5)
        .all()
    )
    top_source_ips = [{"name": ip, "count": cnt} for ip, cnt in top_ips]

    # Top Destination Ports
    top_ports = (
        db.query(TrafficFlow.destination_port, func.count(TrafficFlow.id).label("cnt"))
        .group_by(TrafficFlow.destination_port)
        .order_by(desc("cnt"))
        .limit(5)
        .all()
    )
    top_dest_ports = [{"name": f"Port {port}", "count": cnt} for port, cnt in top_ports]

    # Recent Alerts (top 10)
    recent = db.query(Alert).order_by(desc(Alert.timestamp)).limit(10).all()
    recent_alerts = [a.to_dict() for a in recent]

    # Simple Traffic Timeline (grouped by 1-hour interval or sample points)
    recent_flows = db.query(TrafficFlow).order_by(desc(TrafficFlow.timestamp)).limit(100).all()
    recent_flows.reverse()

    timeline_map = {}
    for f in recent_flows:
        key = f.timestamp.strftime("%H:%M") if f.timestamp else "00:00"
        if key not in timeline_map:
            timeline_map[key] = {"timestamp": key, "total_flows": 0, "normal_flows": 0, "malicious_flows": 0}
        timeline_map[key]["total_flows"] += 1
        if f.prediction in ["BENIGN", "Normal"]:
            timeline_map[key]["normal_flows"] += 1
        else:
            timeline_map[key]["malicious_flows"] += 1

    timeline = list(timeline_map.values())[-15:]

    return {
        "summary": {
            "total_traffic_bytes": total_bytes_res,
            "total_flows": total_flows,
            "normal_traffic_count": normal_count,
            "malicious_traffic_count": malicious_count,
            "critical_alerts_count": critical_alerts,
            "active_threat_level": threat_level
        },
        "traffic_timeline": timeline,
        "attack_distribution": attack_dist,
        "severity_distribution": severity_dist,
        "protocol_distribution": protocol_dist,
        "top_source_ips": top_source_ips,
        "top_dest_ports": top_dest_ports,
        "recent_alerts": recent_alerts
    }

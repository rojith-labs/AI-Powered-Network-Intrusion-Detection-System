from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models.alert import Alert
from app.models.traffic_flow import TrafficFlow

router = APIRouter()

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    # Attack Frequency
    attack_freq = (
        db.query(Alert.attack_type, func.count(Alert.id).label("cnt"))
        .group_by(Alert.attack_type)
        .order_by(desc("cnt"))
        .all()
    )

    # Severity Trends
    sev_counts = (
        db.query(Alert.severity, func.count(Alert.id).label("cnt"))
        .group_by(Alert.severity)
        .all()
    )

    # Protocol breakdown
    proto_counts = (
        db.query(TrafficFlow.protocol, func.count(TrafficFlow.id).label("cnt"))
        .group_by(TrafficFlow.protocol)
        .all()
    )

    # Top Source IPs
    top_src = (
        db.query(Alert.source_ip, func.count(Alert.id).label("cnt"))
        .group_by(Alert.source_ip)
        .order_by(desc("cnt"))
        .limit(8)
        .all()
    )

    # Top Destination Ports
    top_dst_ports = (
        db.query(Alert.destination_port, func.count(Alert.id).label("cnt"))
        .group_by(Alert.destination_port)
        .order_by(desc("cnt"))
        .limit(8)
        .all()
    )

    # Confidence Buckets
    confidence_histogram = [
        {"range": "90% - 100%", "count": db.query(Alert).filter(Alert.confidence >= 0.90).count()},
        {"range": "80% - 89%", "count": db.query(Alert).filter(Alert.confidence >= 0.80, Alert.confidence < 0.90).count()},
        {"range": "70% - 79%", "count": db.query(Alert).filter(Alert.confidence >= 0.70, Alert.confidence < 0.80).count()},
        {"range": "Below 70%", "count": db.query(Alert).filter(Alert.confidence < 0.70).count()}
    ]

    return {
        "attack_frequency": [{"name": name, "count": cnt} for name, cnt in attack_freq],
        "severity_trends": [{"name": name, "count": cnt} for name, cnt in sev_counts],
        "protocol_distribution": [{"name": name, "count": cnt} for name, cnt in proto_counts],
        "top_source_ips": [{"name": ip, "count": cnt} for ip, cnt in top_src],
        "top_dest_ports": [{"name": f"Port {port}", "count": cnt} for port, cnt in top_dst_ports],
        "confidence_histogram": confidence_histogram
    }

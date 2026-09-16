from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.models.alert import Alert

class AlertService:
    @staticmethod
    def create_alert(
        db: Session,
        source_ip: str,
        destination_ip: str,
        protocol: str,
        source_port: int,
        destination_port: int,
        attack_type: str,
        confidence: float,
        threat_score: float,
        severity: str,
        status: str = "New"
    ) -> Alert:
        alert = Alert(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            source_port=source_port,
            destination_port=destination_port,
            attack_type=attack_type,
            confidence=confidence,
            threat_score=threat_score,
            severity=severity,
            status=status
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_alerts(
        db: Session,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        attack_type: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> Tuple[List[Alert], int]:
        query = db.query(Alert)

        if severity:
            query = query.filter(Alert.severity == severity)
        if status:
            query = query.filter(Alert.status == status)
        if attack_type:
            query = query.filter(Alert.attack_type == attack_type)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Alert.source_ip.like(search_pattern),
                    Alert.destination_ip.like(search_pattern),
                    Alert.attack_type.like(search_pattern),
                    Alert.protocol.like(search_pattern)
                )
            )

        total_count = query.count()
        alerts = query.order_by(desc(Alert.timestamp)).offset((page - 1) * limit).limit(limit).all()
        return alerts, total_count

    @staticmethod
    def get_alert_by_id(db: Session, alert_id: int) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def update_alert_status(db: Session, alert_id: int, new_status: str) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            return None
        alert.status = new_status
        db.commit()
        db.refresh(alert)
        return alert

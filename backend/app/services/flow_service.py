from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.models.traffic_flow import TrafficFlow

class FlowService:
    @staticmethod
    def create_flow(
        db: Session,
        source_ip: str,
        destination_ip: str,
        protocol: str,
        source_port: int,
        destination_port: int,
        duration: float,
        packet_count: int,
        byte_count: int,
        prediction: str = "BENIGN",
        threat_score: float = 0.0
    ) -> TrafficFlow:
        flow = TrafficFlow(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            source_port=source_port,
            destination_port=destination_port,
            duration=duration,
            packet_count=packet_count,
            byte_count=byte_count,
            prediction=prediction,
            threat_score=threat_score
        )
        db.add(flow)
        db.commit()
        db.refresh(flow)
        return flow

    @staticmethod
    def get_flows(
        db: Session,
        protocol: Optional[str] = None,
        prediction: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> Tuple[List[TrafficFlow], int]:
        query = db.query(TrafficFlow)

        if protocol:
            query = query.filter(TrafficFlow.protocol == protocol)
        if prediction:
            query = query.filter(TrafficFlow.prediction == prediction)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    TrafficFlow.source_ip.like(pattern),
                    TrafficFlow.destination_ip.like(pattern),
                    TrafficFlow.prediction.like(pattern),
                    TrafficFlow.protocol.like(pattern)
                )
            )

        total_count = query.count()
        flows = query.order_by(desc(TrafficFlow.timestamp)).offset((page - 1) * limit).limit(limit).all()
        return flows, total_count

import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.traffic_flow import TrafficFlow
from app.models.model_metadata import ModelMetadata
from app.services.risk_engine import RiskEngine

def seed_database_if_empty(db: Session):
    # Check if database already has data
    if db.query(Alert).count() > 0 or db.query(TrafficFlow).count() > 0:
        return

    print("[Seeder] Populating initial SOC demo data...")
    now = datetime.now(timezone.utc)

    # Seed Model Metadata
    model_meta = ModelMetadata(
        model_name="XGBoost Classifier",
        version="1.0.0",
        dataset_name="CIC-IDS2017",
        trained_at=now - timedelta(days=2),
        accuracy=0.9967,
        precision=0.9967,
        recall=0.9967,
        f1_score=0.9967,
        status="Active",
        confusion_matrix="[[3623, 0, 0], [1, 712, 0], [0, 0, 620]]"
    )
    db.add(model_meta)

    # Seed Traffic Flows & Alerts over past 24 hours
    sample_ips = [
        "192.168.1.105", "192.168.1.112", "10.0.0.45", "172.16.0.8",
        "45.33.32.156", "185.220.101.4", "198.51.100.22", "203.0.113.88"
    ]
    dest_ips = ["10.0.0.1", "10.0.0.2", "192.168.1.1", "172.16.0.1"]
    protocols = ["TCP", "UDP", "ICMP"]
    attacks = ["BENIGN", "BENIGN", "BENIGN", "DoS", "DDoS", "Port Scan", "Brute Force", "Botnet"]

    for i in range(150):
        ts = now - timedelta(minutes=random.randint(1, 1440))
        src_ip = random.choice(sample_ips)
        dst_ip = random.choice(dest_ips)
        proto = random.choice(protocols)
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([80, 443, 22, 53, 8080, 3389, 445])
        
        attack = random.choice(attacks)
        duration = round(random.uniform(0.01, 15.0), 3)
        pkts = random.randint(1, 500)
        bytes_cnt = pkts * random.randint(64, 1400)

        feats = {
            "packet_rate": pkts / duration,
            "destination_port": dst_port,
            "syn_flag_cnt": random.randint(0, 10),
            "ack_flag_cnt": random.randint(0, 10)
        }

        conf = round(random.uniform(0.85, 0.99), 4) if attack != "BENIGN" else round(random.uniform(0.92, 0.99), 4)
        threat_score, severity = RiskEngine.calculate_threat_score(attack, conf, feats)

        flow = TrafficFlow(
            timestamp=ts,
            source_ip=src_ip,
            destination_ip=dst_ip,
            protocol=proto,
            source_port=src_port,
            destination_port=dst_port,
            duration=duration,
            packet_count=pkts,
            byte_count=bytes_cnt,
            prediction=attack,
            threat_score=threat_score
        )
        db.add(flow)

        if attack != "BENIGN" and threat_score > 20.0:
            status = random.choice(["New", "Investigating", "Resolved", "False Positive"])
            alert = Alert(
                timestamp=ts,
                source_ip=src_ip,
                destination_ip=dst_ip,
                protocol=proto,
                source_port=src_port,
                destination_port=dst_port,
                attack_type=attack,
                confidence=conf,
                threat_score=threat_score,
                severity=severity,
                status=status
            )
            db.add(alert)

    db.commit()
    print("[Seeder] Database seeded successfully!")

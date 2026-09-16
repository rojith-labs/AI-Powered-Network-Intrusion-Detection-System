import asyncio
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime, timezone
from app.ml.predictor import predictor
from app.ml.explainer import NIDSExplainer

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/ws/monitoring")
async def websocket_monitoring_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Simulate live network capture stream for lab environment
        sample_ips = ["192.168.1.105", "10.0.0.12", "172.16.0.4", "45.33.32.156"]
        dest_ips = ["10.0.0.1", "192.168.1.1"]
        attacks = ["BENIGN", "BENIGN", "BENIGN", "DoS", "DDoS", "Port Scan", "Brute Force"]

        while True:
            await asyncio.sleep(2.0)

            src_ip = random.choice(sample_ips)
            dst_ip = random.choice(dest_ips)
            dst_port = random.choice([80, 443, 22, 53, 8080])
            attack_roll = random.choice(attacks)

            feats = {
                "flow_duration": round(random.uniform(0.01, 5.0), 3),
                "fwd_pkts_count": random.randint(1, 100),
                "bwd_pkts_count": random.randint(1, 100),
                "total_bytes": random.randint(100, 10000),
                "packet_rate": round(random.uniform(10.0, 1500.0), 1),
                "destination_port": dst_port,
                "syn_flag_cnt": random.randint(0, 10),
                "ack_flag_cnt": random.randint(0, 10)
            }

            pred, conf, threat_score, severity, importances = predictor.predict_flow(feats)
            exp = NIDSExplainer.generate_explanation(pred, conf, feats)

            event_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": src_ip,
                "destination_ip": dst_ip,
                "protocol": "TCP",
                "source_port": random.randint(1024, 65535),
                "destination_port": dst_port,
                "prediction": pred,
                "confidence": round(conf, 4),
                "threat_score": threat_score,
                "severity": severity,
                "explanation": exp
            }

            await websocket.send_json({"type": "TRAFFIC_FLOW", "data": event_data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

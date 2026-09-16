import os
import sys
import pytest
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.risk_engine import RiskEngine
from app.ml.predictor import predictor
from app.ml.explainer import NIDSExplainer
from app.network.flow_extractor import FlowExtractor
from app.network.packet_parser import PacketParser

def test_risk_engine_benign():
    score, severity = RiskEngine.calculate_threat_score("BENIGN", 0.95, {})
    assert score <= 20.0
    assert severity == "Normal"

def test_risk_engine_ddos():
    feats = {"packet_rate": 1500, "destination_port": 80, "syn_flag_cnt": 20, "ack_flag_cnt": 0}
    score, severity = RiskEngine.calculate_threat_score("DDoS", 0.95, feats)
    assert score >= 80.0
    assert severity == "Critical"

def test_ml_predictor_inference():
    feats = {
        "flow_duration": 1.0,
        "fwd_pkts_count": 100,
        "bwd_pkts_count": 2,
        "total_bytes": 4000,
        "packet_rate": 102.0,
        "syn_flag_cnt": 20,
        "ack_flag_cnt": 0,
        "destination_port": 80,
        "protocol": 6
    }
    pred, conf, score, sev, importances = predictor.predict_flow(feats)
    assert pred in ["BENIGN", "DoS", "DDoS", "Port Scan", "Brute Force", "Botnet"]
    assert 0.0 <= conf <= 1.0
    assert 0.0 <= score <= 100.0
    assert sev in ["Normal", "Low", "Medium", "High", "Critical"]

def test_explainer_indicators():
    feats = {"packet_rate": 600, "syn_flag_cnt": 15, "ack_flag_cnt": 0, "destination_port": 80}
    indicators = NIDSExplainer.generate_explanation("DDoS", 0.94, feats)
    assert len(indicators) > 0

def test_flow_extractor():
    pkts = [
        {
            "src_ip": "192.168.1.10", "dst_ip": "10.0.0.1",
            "src_port": 1234, "dst_port": 80, "protocol": "TCP",
            "protocol_num": 6, "timestamp": 1000.0, "length": 64,
            "flags": {"syn": 1, "ack": 0, "fin": 0, "rst": 0, "psh": 0}
        },
        {
            "src_ip": "192.168.1.10", "dst_ip": "10.0.0.1",
            "src_port": 1234, "dst_port": 80, "protocol": "TCP",
            "protocol_num": 6, "timestamp": 1000.1, "length": 128,
            "flags": {"syn": 0, "ack": 1, "fin": 0, "rst": 0, "psh": 0}
        }
    ]
    flows = FlowExtractor.extract_flows(pkts)
    assert len(flows) == 1
    f = flows[0]
    assert f["fwd_pkts_count"] == 2
    assert f["total_bytes"] == 192

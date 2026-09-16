from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.network.packet_parser import PacketParser
from app.network.flow_extractor import FlowExtractor
from app.ml.predictor import predictor
from app.ml.explainer import NIDSExplainer
from app.services.alert_service import AlertService
from app.services.flow_service import FlowService

class PCAPAnalyzer:
    """
    High-Level PCAP Analysis Pipeline.
    Validates file -> parses packets -> extracts flows -> runs ML predictions ->
    computes threat scores -> persists alerts -> returns structured audit report.
    """

    @classmethod
    def process_file(cls, db: Session, file_path: str, original_filename: str) -> Dict[str, Any]:
        path = Path(file_path)
        file_size = path.stat().st_size if path.exists() else 0

        # Step 1 & 2: Validate & Parse Packets
        parsed_pkts = PacketParser.parse_pcap(file_path)
        total_packets = len(parsed_pkts)

        if total_packets == 0:
            return {
                "filename": original_filename,
                "file_size_bytes": file_size,
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "total_packets": 0,
                "total_flows": 0,
                "normal_flows": 0,
                "suspicious_flows": 0,
                "overall_threat_score": 0.0,
                "overall_severity": "Normal",
                "attack_categories": {},
                "protocol_distribution": {},
                "severity_distribution": {"Normal": 0},
                "alerts_generated": 0,
                "flows": []
            }

        # Step 3: Extract Bidirectional Flows
        flows = FlowExtractor.extract_flows(parsed_pkts)
        total_flows = len(flows)

        normal_count = 0
        suspicious_count = 0
        attack_categories: Dict[str, int] = {}
        protocol_distribution: Dict[str, int] = {}
        severity_distribution: Dict[str, int] = {
            "Normal": 0, "Low": 0, "Medium": 0, "High": 0, "Critical": 0
        }
        alerts_created = 0
        flow_results = []
        max_threat_score = 0.0

        for f in flows:
            # Map protocol
            proto_str = f.get("protocol", "OTHER")
            protocol_distribution[proto_str] = protocol_distribution.get(proto_str, 0) + 1

            # Prepare feature dictionary for ML
            feat_dict = {
                "flow_duration": f["flow_duration"],
                "fwd_pkts_count": f["fwd_pkts_count"],
                "bwd_pkts_count": f["bwd_pkts_count"],
                "total_bytes": f["total_bytes"],
                "packet_rate": f["packet_rate"],
                "bytes_per_sec": f["bytes_per_sec"],
                "avg_pkt_size": f["avg_pkt_size"],
                "min_pkt_size": f["min_pkt_size"],
                "max_pkt_size": f["max_pkt_size"],
                "std_pkt_size": f["std_pkt_size"],
                "fwd_pkt_len_mean": f["fwd_pkt_len_mean"],
                "fwd_pkt_len_std": f["fwd_pkt_len_std"],
                "bwd_pkt_len_mean": f["bwd_pkt_len_mean"],
                "bwd_pkt_len_std": f["bwd_pkt_len_std"],
                "syn_flag_cnt": f["syn_flag_cnt"],
                "ack_flag_cnt": f["ack_flag_cnt"],
                "fin_flag_cnt": f["fin_flag_cnt"],
                "rst_flag_cnt": f["rst_flag_cnt"],
                "psh_flag_cnt": f["psh_flag_cnt"],
                "source_port": f["source_port"],
                "destination_port": f["destination_port"],
                "protocol": f.get("protocol_num", 6),
                "flow_iat_mean": f["flow_iat_mean"],
                "flow_iat_std": f["flow_iat_std"]
            }

            # Step 4: ML Prediction
            pred_class, conf, threat_score, severity, importances = predictor.predict_flow(feat_dict)
            explanation = NIDSExplainer.generate_explanation(pred_class, conf, feat_dict)

            max_threat_score = max(max_threat_score, threat_score)

            if pred_class in ["BENIGN", "Normal"]:
                normal_count += 1
            else:
                suspicious_count += 1
                attack_categories[pred_class] = attack_categories.get(pred_class, 0) + 1

            severity_distribution[severity] = severity_distribution.get(severity, 0) + 1

            # Persist flow in DB
            FlowService.create_flow(
                db=db,
                source_ip=f["source_ip"],
                destination_ip=f["destination_ip"],
                protocol=proto_str,
                source_port=f["source_port"],
                destination_port=f["destination_port"],
                duration=f["flow_duration"],
                packet_count=f["fwd_pkts_count"] + f["bwd_pkts_count"],
                byte_count=f["total_bytes"],
                prediction=pred_class,
                threat_score=threat_score
            )

            # Generate Alert if threat score > 20 (Medium, High, Critical)
            if threat_score > 20.0 and pred_class not in ["BENIGN", "Normal"]:
                AlertService.create_alert(
                    db=db,
                    source_ip=f["source_ip"],
                    destination_ip=f["destination_ip"],
                    protocol=proto_str,
                    source_port=f["source_port"],
                    destination_port=f["destination_port"],
                    attack_type=pred_class,
                    confidence=conf,
                    threat_score=threat_score,
                    severity=severity,
                    status="New"
                )
                alerts_created += 1

            flow_results.append({
                "timestamp": datetime.fromtimestamp(f["start_time"], timezone.utc).isoformat(),
                "source_ip": f["source_ip"],
                "destination_ip": f["destination_ip"],
                "protocol": proto_str,
                "source_port": f["source_port"],
                "destination_port": f["destination_port"],
                "duration": f["flow_duration"],
                "packet_count": f["fwd_pkts_count"] + f["bwd_pkts_count"],
                "byte_count": f["total_bytes"],
                "prediction": pred_class,
                "confidence": round(conf, 4),
                "threat_score": threat_score,
                "severity": severity,
                "explanation": explanation
            })

        # Overall severity
        if max_threat_score <= 20.0:
            overall_severity = "Normal"
        elif max_threat_score <= 40.0:
            overall_severity = "Low"
        elif max_threat_score <= 60.0:
            overall_severity = "Medium"
        elif max_threat_score <= 80.0:
            overall_severity = "High"
        else:
            overall_severity = "Critical"

        return {
            "filename": original_filename,
            "file_size_bytes": file_size,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "total_packets": total_packets,
            "total_flows": total_flows,
            "normal_flows": normal_count,
            "suspicious_flows": suspicious_count,
            "overall_threat_score": max_threat_score,
            "overall_severity": overall_severity,
            "attack_categories": attack_categories,
            "protocol_distribution": protocol_distribution,
            "severity_distribution": severity_distribution,
            "alerts_generated": alerts_created,
            "flows": flow_results
        }

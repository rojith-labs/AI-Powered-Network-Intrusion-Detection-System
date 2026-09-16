from typing import Dict, Any, List

class NIDSExplainer:
    """
    Explainable AI (XAI) engine for AI-NIDS.
    Generates human-understandable indicators and feature attribution lists.
    """

    @staticmethod
    def generate_explanation(
        prediction: str,
        confidence: float,
        features: Dict[str, Any]
    ) -> List[str]:
        indicators = []

        pkt_rate = float(features.get("packet_rate", 0))
        duration = float(features.get("flow_duration", 0))
        syn_cnt = int(features.get("syn_flag_cnt", 0))
        ack_cnt = int(features.get("ack_flag_cnt", 0))
        rst_cnt = int(features.get("rst_flag_cnt", 0))
        dst_port = int(features.get("destination_port", 0))
        total_bytes = int(features.get("total_bytes", 0))

        if prediction in ["BENIGN", "Normal"]:
            indicators.append("Flow statistics match normal network baseline behavior.")
            indicators.append("Standard TCP/UDP handshake and standard byte transfer rates.")
            return indicators

        if prediction in ["DoS", "DDoS"]:
            if pkt_rate > 500:
                indicators.append(f"Abnormally high packet rate detected ({pkt_rate:.1f} pkts/sec).")
            if syn_cnt > 10 and ack_cnt == 0:
                indicators.append(f"Excessive SYN flags without ACK response ({syn_cnt} SYN packets).")
            if total_bytes < 5000 and float(features.get("fwd_pkts_count", 0)) > 50:
                indicators.append("Asymmetric flow with high forward packet count and low total payload.")
            indicators.append(f"Targeted service port: {dst_port}.")

        elif prediction == "Port Scan":
            if duration < 0.2:
                indicators.append(f"Extremely short flow duration ({duration * 1000:.1f} ms).")
            if syn_cnt == 1 and ack_cnt == 0:
                indicators.append("Single SYN probe packet detected without session establishment.")
            indicators.append(f"Probe targeting port {dst_port}.")

        elif prediction == "Brute Force":
            indicators.append(f"Repeated connection attempts to authentication port {dst_port}.")
            if duration > 0.5 and float(features.get("fwd_pkts_count", 0)) > 15:
                indicators.append("Multiple rapid sequential handshake iterations in single flow window.")

        elif prediction == "Botnet":
            indicators.append(f"High payload volume ({total_bytes} bytes) to command-and-control port {dst_port}.")
            indicators.append("Sustained bidirectional TCP keep-alive connection profile.")

        else:
            indicators.append(f"Anomalous traffic pattern detected with {confidence * 100:.1f}% confidence.")
            if rst_cnt > 0:
                indicators.append(f"Contains {rst_cnt} RST connection termination flags.")

        if not indicators:
            indicators.append("Model identified feature pattern deviation from standard traffic profile.")

        return indicators

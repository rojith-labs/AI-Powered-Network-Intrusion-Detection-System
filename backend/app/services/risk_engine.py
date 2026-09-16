from typing import Dict, Any, Tuple

class RiskEngine:
    """
    Project-defined Risk Scoring Engine (0-100)
    
    This is a project-defined risk score combining model classification confidence
    and domain-specific network rule heuristics.
    It is NOT an industry-standard severity rating (like CVSS).
    """

    # Base risk weights per attack category
    CATEGORY_BASE_RISK: Dict[str, float] = {
        "BENIGN": 5.0,
        "Normal": 5.0,
        "DoS": 75.0,
        "DDoS": 85.0,
        "Port Scan": 55.0,
        "Brute Force": 65.0,
        "Botnet": 90.0,
        "Web Attack": 70.0,
        "Infiltration": 95.0,
        "Other": 50.0
    }

    # Sensitive destination ports
    CRITICAL_PORTS = {22, 23, 80, 443, 445, 1433, 3306, 3389, 8080}

    @classmethod
    def calculate_threat_score(
        cls,
        prediction: str,
        confidence: float,
        features: Dict[str, Any]
    ) -> Tuple[float, str]:
        """
        Calculates a 0-100 Threat Score and maps it to a Severity level.
        
        Severity Bands:
          0 - 20:   Normal
          21 - 40:  Low
          41 - 60:  Medium
          61 - 80:  High
          81 - 100: Critical
        """
        if prediction in ["BENIGN", "Normal"]:
            base = cls.CATEGORY_BASE_RISK.get(prediction, 5.0)
            score = base * confidence
            return round(min(score, 20.0), 1), "Normal"

        # Start from base risk of attack category
        base_score = cls.CATEGORY_BASE_RISK.get(prediction, 60.0)

        # Scale by prediction confidence
        score = base_score * (0.5 + 0.5 * confidence)

        # Heuristic 1: High packet rate / byte volume boost
        packet_rate = float(features.get("packet_rate", 0))
        if packet_rate > 1000:
            score += 10.0
        elif packet_rate > 100:
            score += 5.0

        # Heuristic 2: Sensitive destination port targeting
        dst_port = int(features.get("destination_port", 0))
        if dst_port in cls.CRITICAL_PORTS:
            score += 5.0

        # Heuristic 3: TCP Flag anomalies (e.g. SYN flood without ACK or FIN/RST floods)
        syn_cnt = int(features.get("syn_flag_cnt", 0))
        ack_cnt = int(features.get("ack_flag_cnt", 0))
        rst_cnt = int(features.get("rst_flag_cnt", 0))
        if syn_cnt > 10 and ack_cnt == 0:
            score += 10.0
        if rst_cnt > 5:
            score += 5.0

        # Clamp score between 0 and 100
        final_score = round(max(0.0, min(100.0, score)), 1)

        # Determine severity band
        if final_score <= 20.0:
            severity = "Normal"
        elif final_score <= 40.0:
            severity = "Low"
        elif final_score <= 60.0:
            severity = "Medium"
        elif final_score <= 80.0:
            severity = "High"
        else:
            severity = "Critical"

        return final_score, severity

import numpy as np
from typing import List, Dict, Any

class FlowExtractor:
    """
    Bidirectional Flow Feature Extractor for AI-NIDS.
    Aggregates packet headers into 5-tuple network flows and computes statistical features.
    """

    @classmethod
    def extract_flows(cls, parsed_packets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not parsed_packets:
            return []

        flows_map = {}

        for pkt in parsed_packets:
            src_ip = pkt["src_ip"]
            dst_ip = pkt["dst_ip"]
            src_port = pkt["src_port"]
            dst_port = pkt["dst_port"]
            proto_num = pkt["protocol_num"]

            # Canonical 5-tuple key
            if (src_ip, src_port) <= (dst_ip, dst_port):
                flow_key = (src_ip, dst_ip, src_port, dst_port, proto_num)
            else:
                flow_key = (dst_ip, src_ip, dst_port, src_port, proto_num)

            if flow_key not in flows_map:
                flows_map[flow_key] = {
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": pkt["protocol"],
                    "protocol_num": proto_num,
                    "timestamps": [],
                    "fwd_lengths": [],
                    "bwd_lengths": [],
                    "syn_count": 0,
                    "ack_count": 0,
                    "fin_count": 0,
                    "rst_count": 0,
                    "psh_count": 0
                }

            f = flows_map[flow_key]
            direction = "forward" if (src_ip == f["src_ip"] and src_port == f["src_port"]) else "backward"
            f["timestamps"].append(pkt["timestamp"])
            if direction == "forward":
                f["fwd_lengths"].append(pkt["length"])
            else:
                f["bwd_lengths"].append(pkt["length"])

            flags = pkt["flags"]
            f["syn_count"] += flags["syn"]
            f["ack_count"] += flags["ack"]
            f["fin_count"] += flags["fin"]
            f["rst_count"] += flags["rst"]
            f["psh_count"] += flags["psh"]

        extracted_flows = []
        for key, f in flows_map.items():
            ts = f["timestamps"]
            ts.sort()
            duration = max(0.0001, ts[-1] - ts[0])

            fwd_lens = f["fwd_lengths"] if f["fwd_lengths"] else [0]
            bwd_lens = f["bwd_lengths"] if f["bwd_lengths"] else [0]
            all_lens = fwd_lens + bwd_lens

            fwd_count = len(f["fwd_lengths"])
            bwd_count = len(f["bwd_lengths"])
            total_pkts = fwd_count + bwd_count
            total_bytes = sum(all_lens)

            # Inter-arrival times
            iats = [ts[i] - ts[i-1] for i in range(1, len(ts))] if len(ts) > 1 else [0.0]

            flow_dict = {
                "source_ip": f["src_ip"],
                "destination_ip": f["dst_ip"],
                "source_port": f["src_port"],
                "destination_port": f["dst_port"],
                "protocol": f["protocol"],
                "flow_duration": round(duration, 4),
                "fwd_pkts_count": fwd_count,
                "bwd_pkts_count": bwd_count,
                "total_bytes": total_bytes,
                "packet_rate": round(total_pkts / duration, 2),
                "bytes_per_sec": round(total_bytes / duration, 2),
                "avg_pkt_size": round(float(np.mean(all_lens)), 2),
                "min_pkt_size": float(np.min(all_lens)),
                "max_pkt_size": float(np.max(all_lens)),
                "std_pkt_size": round(float(np.std(all_lens)), 2),
                "fwd_pkt_len_mean": round(float(np.mean(fwd_lens)), 2),
                "fwd_pkt_len_std": round(float(np.std(fwd_lens)), 2),
                "bwd_pkt_len_mean": round(float(np.mean(bwd_lens)), 2),
                "bwd_pkt_len_std": round(float(np.std(bwd_lens)), 2),
                "syn_flag_cnt": f["syn_count"],
                "ack_flag_cnt": f["ack_count"],
                "fin_flag_cnt": f["fin_count"],
                "rst_flag_cnt": f["rst_count"],
                "psh_flag_cnt": f["psh_count"],
                "protocol_num": f["protocol_num"],
                "flow_iat_mean": round(float(np.mean(iats)), 4),
                "flow_iat_std": round(float(np.std(iats)), 4),
                "start_time": ts[0]
            }

            extracted_flows.append(flow_dict)

        return extracted_flows

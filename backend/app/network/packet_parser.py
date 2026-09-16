import os
from typing import List, Dict, Any, Tuple
from pathlib import Path
from scapy.all import rdpcap, IP, IPv6, TCP, UDP, ICMP, Scapy_Exception

class PacketParser:
    """
    Safe PCAP and PCAPNG Packet Parser using Scapy.
    Extracts header metadata while ignoring/preventing execution of packet payloads.
    """

    SUPPORTED_EXTENSIONS = [".pcap", ".pcapng"]

    @classmethod
    def validate_file(cls, file_path: str, max_size_bytes: int = 50 * 1024 * 1024) -> Tuple[bool, str]:
        path = Path(file_path)
        if not path.exists():
            return False, "File does not exist."

        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            return False, f"Unsupported file extension '{path.suffix}'. Only .pcap and .pcapng are supported."

        size = path.stat().st_size
        if size == 0:
            return False, "File is empty (0 bytes)."

        if size > max_size_bytes:
            return False, f"File size ({size / 1024 / 1024:.1f} MB) exceeds maximum limit of {max_size_bytes / 1024 / 1024} MB."

        return True, "Valid file."

    @classmethod
    def parse_pcap(cls, file_path: str) -> List[Dict[str, Any]]:
        """
        Parses a PCAP/PCAPNG file and returns a list of packet header dictionaries.
        """
        valid, msg = cls.validate_file(file_path)
        if not valid:
            raise ValueError(msg)

        parsed_packets = []
        try:
            packets = rdpcap(file_path)
        except Scapy_Exception as e:
            raise ValueError(f"Corrupted or invalid PCAP file format: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to read PCAP file: {str(e)}")

        for idx, pkt in enumerate(packets):
            pkt_dict = {
                "id": idx + 1,
                "timestamp": float(pkt.time),
                "length": len(pkt),
                "src_ip": "0.0.0.0",
                "dst_ip": "0.0.0.0",
                "protocol": "OTHER",
                "protocol_num": 0,
                "src_port": 0,
                "dst_port": 0,
                "flags": {
                    "syn": 0, "ack": 0, "fin": 0, "rst": 0, "psh": 0
                }
            }

            if IP in pkt:
                pkt_dict["src_ip"] = pkt[IP].src
                pkt_dict["dst_ip"] = pkt[IP].dst
                pkt_dict["protocol_num"] = int(pkt[IP].proto)
            elif IPv6 in pkt:
                pkt_dict["src_ip"] = pkt[IPv6].src
                pkt_dict["dst_ip"] = pkt[IPv6].dst
                pkt_dict["protocol_num"] = int(pkt[IPv6].nh)

            if TCP in pkt:
                pkt_dict["protocol"] = "TCP"
                pkt_dict["src_port"] = int(pkt[TCP].sport)
                pkt_dict["dst_port"] = int(pkt[TCP].dport)
                flags = pkt[TCP].flags
                pkt_dict["flags"]["syn"] = 1 if "S" in flags else 0
                pkt_dict["flags"]["ack"] = 1 if "A" in flags else 0
                pkt_dict["flags"]["fin"] = 1 if "F" in flags else 0
                pkt_dict["flags"]["rst"] = 1 if "R" in flags else 0
                pkt_dict["flags"]["psh"] = 1 if "P" in flags else 0
            elif UDP in pkt:
                pkt_dict["protocol"] = "UDP"
                pkt_dict["src_port"] = int(pkt[UDP].sport)
                pkt_dict["dst_port"] = int(pkt[UDP].dport)
            elif ICMP in pkt:
                pkt_dict["protocol"] = "ICMP"

            parsed_packets.append(pkt_dict)

        return parsed_packets

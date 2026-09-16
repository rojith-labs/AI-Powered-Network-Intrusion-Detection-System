import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Network Intrusion Detection System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Paths
    UPLOAD_DIR: Path = BACKEND_DIR / "uploads"
    MODEL_DIR: Path = BACKEND_DIR / "models"
    DATASET_DIR: Path = BACKEND_DIR / "datasets"
    DATABASE_URL: str = f"sqlite:///{BACKEND_DIR}/nids.db"
    
    # File Limits
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS: list[str] = [".pcap", ".pcapng"]
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ]
    
    # Feature list matching CIC-IDS2017 flow statistics
    FEATURE_NAMES: list[str] = [
        "flow_duration",
        "fwd_pkts_count",
        "bwd_pkts_count",
        "total_bytes",
        "packet_rate",
        "bytes_per_sec",
        "avg_pkt_size",
        "min_pkt_size",
        "max_pkt_size",
        "std_pkt_size",
        "fwd_pkt_len_mean",
        "fwd_pkt_len_std",
        "bwd_pkt_len_mean",
        "bwd_pkt_len_std",
        "syn_flag_cnt",
        "ack_flag_cnt",
        "fin_flag_cnt",
        "rst_flag_cnt",
        "psh_flag_cnt",
        "source_port",
        "destination_port",
        "protocol",
        "flow_iat_mean",
        "flow_iat_std"
    ]
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure required directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.DATASET_DIR, exist_ok=True)

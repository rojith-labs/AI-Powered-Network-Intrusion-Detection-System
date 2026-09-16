# Machine Learning Pipeline Documentation

## Dataset & Feature Extraction

The system utilizes flow statistical features aligned with the standard **CIC-IDS2017** network intrusion dataset schema:

- `flow_duration`: Total duration of the network flow in seconds.
- `fwd_pkts_count`, `bwd_pkts_count`: Total packets sent in forward and backward directions.
- `total_bytes`: Sum of bytes transferred.
- `packet_rate`, `bytes_per_sec`: Throughput intensity statistics.
- `avg_pkt_size`, `min_pkt_size`, `max_pkt_size`, `std_pkt_size`: Packet size distribution metrics.
- `syn_flag_cnt`, `ack_flag_cnt`, `fin_flag_cnt`, `rst_flag_cnt`, `psh_flag_cnt`: Control flag counts.
- `destination_port`, `protocol`: Transport layer identifiers.

## Model Benchmarks

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **XGBoost Classifier** | **99.67%** | **99.67%** | **99.67%** | **99.67%** | **1.0000** |
| Random Forest | 99.60% | 99.60% | 99.60% | 99.60% | 1.0000 |
| Logistic Regression | 98.73% | 98.75% | 98.73% | 98.73% | 0.9998 |

*Selected Model*: **XGBoost Classifier** saved via `joblib` artifact.

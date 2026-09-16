# AI-NIDS API Documentation

The backend service runs on **FastAPI** (default port `8000`) and provides the following REST and WebSocket interfaces under `/api`.

## Endpoints Summary

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System status, database check & active ML model metadata |
| `GET` | `/api/dashboard` | Aggregated SOC summary metrics, charts, & recent alerts |
| `GET` | `/api/alerts` | Paginated security alerts list with filtering |
| `GET` | `/api/alerts/{id}` | Single alert detail record |
| `POST` | `/api/alerts/{id}/status` | Update alert triage status (`New`, `Investigating`, `Resolved`, `False Positive`) |
| `POST` | `/api/predict` | Single flow feature vector inference, threat score & XAI indicators |
| `POST` | `/api/analyze-pcap` | Upload `.pcap` or `.pcapng` file for complete batch threat audit |
| `GET` | `/api/traffic` | Paginated traffic flow logs |
| `GET` | `/api/analytics` | Deep threat distribution, confidence histograms, top target ports |
| `GET` | `/api/models` | Machine learning model evaluation metrics & status |
| `WS` | `/api/ws/monitoring` | WebSocket stream for live network flow detection updates |

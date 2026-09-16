# Final Year Project Report: AI-Powered Network Intrusion Detection System (AI-NIDS)

## Abstract
This project presents an enterprise-grade defensive Security Operations Center (SOC) platform designed for authorized lab network environments. Utilizing machine learning models (XGBoost, Random Forest, Logistic Regression) trained on CIC-IDS2017 flow statistics, the system ingests PCAP captures, extracts bidirectional flow features, classifies attack vectors, and calculates transparent 0-100 threat scores with Explainable AI (XAI) feature attributions.

## Author & Project Metadata
- **Project Title**: AI-Powered Network Intrusion Detection System (AI-NIDS)
- **Architecture**: Asynchronous FastAPI Backend, SQLite Database, React (Vite + Tailwind CSS) Dashboard.
- **Evaluation F1 Score**: 99.67% (XGBoost Classifier)

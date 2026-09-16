# 🛡️ AI-Powered Network Intrusion Detection System

> An intelligent, machine-learning-based defensive cybersecurity platform for detecting, classifying, analyzing, and visualizing suspicious network activity.

![AI-NIDS](https://img.shields.io/badge/AI--NIDS-Network%20Security-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-purple)

---

# 📌 Table of Contents

* [Overview](#-overview)
* [Problem Statement](#-problem-statement)
* [Why This Project](#-why-this-project)
* [Objectives](#-objectives)
* [Key Features](#-key-features)
* [How the System Works](#-how-the-system-works)
* [System Architecture](#-system-architecture)
* [Machine Learning Pipeline](#-machine-learning-pipeline)
* [Network Traffic Analysis](#-network-traffic-analysis)
* [Attack Detection](#-attack-detection)
* [Threat Scoring](#-threat-scoring)
* [Explainable AI](#-explainable-ai)
* [PCAP Analysis](#-pcap-analysis)
* [Real-Time Monitoring](#-real-time-monitoring)
* [SOC Dashboard](#-soc-dashboard)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Dataset](#-dataset)
* [Installation](#-installation)
* [Backend Setup](#-backend-setup)
* [Frontend Setup](#-frontend-setup)
* [ML Model Training](#-ml-model-training)
* [Running the Application](#-running-the-application)
* [API Documentation](#-api-documentation)
* [Database](#-database)
* [Testing](#-testing)
* [Example Workflow](#-example-workflow)
* [Security](#-security)
* [Limitations](#-limitations)
* [Future Enhancements](#-future-enhancements)
* [Project Use Cases](#-project-use-cases)
* [Learning Outcomes](#-learning-outcomes)
* [Ethical Use](#-ethical-use)
* [Conclusion](#-conclusion)
* [Author](#-author)

---

# 🚀 Overview

**AI-Powered Network Intrusion Detection System (AI-NIDS)** is a defensive cybersecurity application that combines **Artificial Intelligence, Machine Learning, network traffic analysis, and a Security Operations Center (SOC)-style web dashboard**.

Traditional intrusion detection systems often rely heavily on predefined signatures and manually configured rules. These approaches can be useful for known threats but may have difficulty identifying previously unseen or changing traffic patterns.

AI-NIDS approaches the problem using machine learning.

The system analyzes network traffic, extracts meaningful network-flow characteristics, and provides a machine-learning prediction about whether the traffic appears normal or suspicious.

When suspicious activity is identified, the system can:

* Classify the traffic into an available attack category.
* Calculate model confidence.
* Generate a project-defined threat score.
* Assign a severity level.
* Create a security alert.
* Store the event in a database.
* Display the event through a web-based SOC dashboard.
* Provide analytical information about detected traffic.

The project is designed primarily for **authorized networks, cybersecurity laboratories, educational environments, and defensive security research**.

---

# 🎯 Problem Statement

Modern networks generate a huge amount of traffic every second.

Manually examining every network connection is impractical.

A security analyst may need to determine:

* Which traffic is normal?
* Which traffic is suspicious?
* Which source is generating unusual activity?
* What type of attack might be occurring?
* How severe is the event?
* How confident is the detection?
* Which network characteristics contributed to the prediction?

A system that automatically analyzes traffic and highlights potentially malicious patterns can help reduce the amount of manual analysis required.

Therefore, this project aims to develop an AI-powered network intrusion detection platform capable of analyzing network-flow information and presenting potential security events in an understandable dashboard.

---

# 💡 Why This Project?

This project combines two major areas:

### 🤖 Artificial Intelligence / Machine Learning

Machine learning is used to identify patterns in network traffic.

### 🛡️ Cybersecurity

The system applies those predictions to defensive network monitoring and security alerting.

This combination makes the project useful for demonstrating practical knowledge in:

* Artificial Intelligence
* Machine Learning
* Cybersecurity
* Network Security
* Data Science
* Backend Development
* Frontend Development
* Database Management
* Data Visualization
* Explainable AI

---

# 🎯 Objectives

The main objectives are:

1. Build an intelligent network intrusion detection platform.
2. Analyze network traffic using flow-level information.
3. Extract useful features from network traffic.
4. Train machine-learning models using cybersecurity datasets.
5. Detect normal and suspicious traffic.
6. Classify available attack categories.
7. Calculate a transparent project-defined risk score.
8. Generate security alerts.
9. Store detection information in a database.
10. Provide an interactive SOC-style web dashboard.
11. Support PCAP file analysis.
12. Provide model performance analysis.
13. Implement basic Explainable AI.
14. Provide a foundation for optional authorized real-time monitoring.

---

# ✨ Key Features

## 🖥️ 1. SOC Dashboard

The dashboard provides a centralized view of network security.

It displays:

* Total packets
* Total flows
* Normal traffic
* Suspicious traffic
* Security alerts
* Critical alerts
* Attack distribution
* Traffic trends
* Protocol distribution
* Recent alerts

---

## 📦 2. PCAP Analysis

Users can upload:

```text
.pcap
.pcapng
```

The system processes the capture and extracts network-flow information.

The result can include:

* Packet count
* Flow count
* Traffic statistics
* Predictions
* Attack categories
* Confidence
* Threat score
* Severity

---

## 🤖 3. Machine Learning Detection

The system supports multiple ML algorithms.

Examples:

* Logistic Regression
* Random Forest
* XGBoost
* MLP Neural Network

Models are trained and evaluated using actual dataset results.

The system does not hard-code detection results or fabricate model accuracy.

---

## 🚨 4. Attack Classification

Depending on the selected dataset, the system can work with categories such as:

* BENIGN
* DoS
* DDoS
* Port Scan
* Brute Force
* Botnet
* Web Attack
* Infiltration
* Other

The exact labels depend on the dataset used for training.

---

## 🎯 5. Threat Score

The application calculates a project-defined score between:

```text
0 – 100
```

Example severity mapping:

|  Score | Severity |
| -----: | -------- |
|   0–20 | Normal   |
|  21–40 | Low      |
|  41–60 | Medium   |
|  61–80 | High     |
| 81–100 | Critical |

This score is a project-specific risk indicator and should not be interpreted as an industry-standard severity score.

---

# 🔄 How the System Works

The complete workflow is:

```text
Network Traffic / PCAP
          │
          ▼
     Packet Parsing
          │
          ▼
     Flow Generation
          │
          ▼
   Feature Extraction
          │
          ▼
    Data Preprocessing
          │
          ▼
      ML Prediction
          │
          ▼
 ┌────────┴─────────┐
 │                  │
 ▼                  ▼
Normal          Suspicious
                    │
                    ▼
             Attack Classification
                    │
                    ▼
              Threat Scoring
                    │
                    ▼
              Alert Generation
                    │
                    ▼
                 Database
                    │
                    ▼
              SOC Dashboard
```

---

# 🏗️ System Architecture

```text
                  ┌──────────────────────┐
                  │   Network Traffic    │
                  │      / PCAP          │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │   Network Analyzer   │
                  │      Scapy/PCAP      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Feature Extraction   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ ML Preprocessing     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    ML Classifier     │
                  │ Random Forest/XGB    │
                  └──────────┬───────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                 Normal           Suspicious
                                      │
                                      ▼
                              ┌──────────────┐
                              │ Risk Engine  │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Alert Engine │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │   SQLite DB  │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ React SOC UI │
                              └──────────────┘
```

---

# 🧠 Machine Learning Pipeline

The ML pipeline contains the following stages:

```text
Dataset
   ↓
Data Loading
   ↓
Data Cleaning
   ↓
Missing Value Handling
   ↓
Duplicate Handling
   ↓
Label Processing
   ↓
Feature Selection
   ↓
Encoding
   ↓
Scaling
   ↓
Train/Test Split
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Selection
   ↓
Model Serialization
   ↓
FastAPI Integration
   ↓
Prediction
```

---

# 🧹 Data Preprocessing

Raw cybersecurity datasets can contain:

* Missing values
* Infinite values
* Duplicate records
* Different data types
* Categorical features
* Highly imbalanced classes
* Dataset-specific column names

The preprocessing pipeline handles these conditions before model training.

Typical preprocessing operations include:

1. Remove invalid values.
2. Handle missing values.
3. Remove duplicates where appropriate.
4. Encode categorical information.
5. Select useful features.
6. Scale numerical features where required.
7. Split the dataset.
8. Train the ML model.

The exact preprocessing steps depend on the dataset.

---

# 🔬 Network Traffic Analysis

The system converts packet-level information into useful flow-level characteristics.

Examples include:

```text
Flow Duration
Forward Packet Count
Backward Packet Count
Total Bytes
Packet Rate
Bytes per Second
Average Packet Size
Minimum Packet Size
Maximum Packet Size
SYN Count
ACK Count
FIN Count
RST Count
Source Port
Destination Port
Protocol
Inter-arrival Time
```

These features provide the ML model with numerical information about network behavior.

---

# 🚨 Attack Detection

Suppose the system analyzes a flow:

```text
Packet Count      : Very High
Packet Rate       : Very High
Flow Duration     : Abnormal
SYN Count         : High
Destination Port  : 443
```

The ML model processes the features.

Example output:

```text
Prediction  : DDoS
Confidence  : 94.2%
```

The application then sends this information to the risk engine.

Important:

The model's prediction represents a machine-learning classification and should not automatically be treated as proof of an actual attack.

---

# 🎯 Threat Scoring

The system combines prediction information with configurable indicators.

Example:

```text
Prediction     : DDoS
Confidence     : 94.2%
Threat Score   : 92
Severity       : Critical
```

The scoring system is designed to make the dashboard easier to understand.

It is not intended to replace a professional incident-response process.

---

# 🧠 Explainable AI

Machine-learning predictions can sometimes be difficult to understand.

Therefore, the project includes basic explainability.

For tree-based models, the system can use:

* Feature importance
* SHAP explanations where practical

Example:

```text
Prediction:
DDoS

Confidence:
94.2%

Important Indicators:

• High packet rate
• High packet count
• Abnormal flow duration
• High SYN activity
```

These indicators explain which features influenced the model rather than proving that an attack occurred.

---

# 📦 PCAP Analysis

PCAP analysis allows users to analyze previously captured network traffic.

Workflow:

```text
Select PCAP
     ↓
Upload
     ↓
Validate
     ↓
Parse packets
     ↓
Create network flows
     ↓
Extract features
     ↓
Run ML model
     ↓
Generate predictions
     ↓
Calculate threat scores
     ↓
Generate alerts
     ↓
Display results
```

The system must never execute packet payloads.

---

# ⚡ Real-Time Monitoring

The project can optionally support authorized local/lab network monitoring.

Possible technologies include:

* Scapy
* WebSocket
* Flow aggregation
* ML inference

The dashboard can provide:

```text
START MONITORING
STOP MONITORING
```

During monitoring, the dashboard can update:

* Packet count
* Flow count
* Detection count
* Suspicious traffic
* Security alerts

Real-time monitoring must only be used on networks and interfaces where the user has authorization.

---

# 🖥️ SOC Dashboard

The frontend is designed as a modern Security Operations Center interface.

## Dashboard Components

### Security Overview

```text
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Packets    │    Flows     │  Suspicious  │   Alerts     │
│    25,430    │    1,842     │     121      │      18      │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

### Traffic Timeline

Shows how traffic changes over time.

### Attack Distribution

Shows detected attack categories.

### Severity Distribution

Displays:

```text
Normal
Low
Medium
High
Critical
```

### Recent Alerts

Example:

```text
Attack     Source IP       Score     Severity
------------------------------------------------
DDoS       192.168.1.15    92        Critical
Scan       192.168.1.25    71        High
Brute      192.168.1.30    64        High
```

---

# 🛠️ Technology Stack

## Frontend

* React
* Vite
* Tailwind CSS
* Recharts
* Lucide React
* Axios

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy

## AI / ML

* Scikit-learn
* XGBoost
* Pandas
* NumPy
* Joblib
* SHAP

## Network

* Scapy
* PCAP
* PCAPNG

## Database

* SQLite

## Development

* Git
* GitHub
* VS Code / Antigravity IDE

---

# 📁 Project Structure

```text
ai-nids/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── alert.py
│   │   │   ├── prediction.py
│   │   │   └── traffic.py
│   │   │
│   │   ├── schemas/
│   │   ├── api/
│   │   ├── services/
│   │   ├── ml/
│   │   ├── network/
│   │   └── utils/
│   │
│   ├── models/
│   ├── datasets/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── ml/
│   ├── preprocessing/
│   ├── training/
│   ├── evaluation/
│   └── saved_models/
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── ml-pipeline.md
│   └── project-report.md
│
├── README.md
├── .gitignore
└── docker-compose.yml
```

---

# 📊 Dataset

The project can be adapted to publicly available cybersecurity datasets.

Recommended datasets include:

## CIC-IDS2017

A widely used intrusion-detection dataset containing benign and malicious network traffic.

## CSE-CIC-IDS2018

A larger cybersecurity dataset suitable for intrusion-detection experiments.

## UNSW-NB15

Another commonly used dataset for network intrusion detection research.

The application should not assume that every dataset contains the same columns or attack classes.

A dataset adapter should map the selected dataset to the project's internal feature schema.

---

# ⚙️ Installation

## Requirements

Install:

```text
Python 3.11+
Node.js 18+
npm
Git
```

For optional packet-capture functionality, a compatible packet-analysis environment may also be required.

---

# 🐍 Backend Setup

Navigate to backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python -m app.database
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Frontend Setup

Open another terminal.

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend will normally be available through the Vite development URL shown in the terminal.

---

# 🧠 ML Model Training

Place the selected dataset in:

```text
backend/datasets/
```

Run the training pipeline:

```bash
python -m ml.training.train
```

The pipeline should:

1. Load the dataset.
2. Clean the data.
3. Prepare features.
4. Split the dataset.
5. Train models.
6. Evaluate models.
7. Compare metrics.
8. Save the selected model.

Example output:

```text
Loading dataset...

Dataset loaded successfully.

Preprocessing...
Training Logistic Regression...
Training Random Forest...
Training XGBoost...

Evaluation completed.

Best model:
XGBoost

Model saved successfully.
```

Actual metrics must be generated from the dataset.

---

# ▶️ Running the Application

Start the backend:

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Start frontend:

```bash
cd frontend
npm run dev
```

Then open the frontend using the URL displayed by Vite.

---

# 🔌 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
/docs
```

Important endpoints:

```text
GET  /api/health

GET  /api/dashboard

GET  /api/alerts

GET  /api/alerts/{id}

POST /api/alerts/{id}/status

POST /api/predict

POST /api/analyze-pcap

GET  /api/traffic

GET  /api/analytics

GET  /api/models
```

---

# 🗄️ Database

The project uses SQLite for development.

Main tables:

## Alerts

Stores detected security events.

Fields include:

```text
ID
Timestamp
Source IP
Destination IP
Protocol
Source Port
Destination Port
Attack Type
Confidence
Threat Score
Severity
Status
```

## Predictions

Stores ML predictions.

```text
ID
Timestamp
Model
Prediction
Confidence
Threat Score
Features
```

## Traffic Flows

Stores flow statistics.

```text
ID
Timestamp
Source IP
Destination IP
Protocol
Duration
Packet Count
Byte Count
```

---

# 🧪 Testing

Run:

```bash
pytest
```

Test:

* Feature extraction
* Dataset preprocessing
* Model prediction
* Threat scoring
* Database operations
* Alert creation
* API endpoints
* PCAP validation

The application should not be considered production-ready solely because tests pass; security validation and operational testing are still required.

---

# 🔄 Example Workflow

## Step 1 — Start Application

Open the AI-NIDS dashboard.

```text
SYSTEM STATUS: ONLINE
```

---

## Step 2 — Upload PCAP

User uploads:

```text
network_capture.pcap
```

---

## Step 3 — Analyze

System processes:

```text
25,430 packets
1,842 flows
```

---

## Step 4 — ML Prediction

Example:

```text
Normal:
1,721

Suspicious:
121
```

---

## Step 5 — Attack Classification

Example:

```text
DDoS
Port Scan
Brute Force
```

---

## Step 6 — Threat Score

Example:

```text
DDoS
Confidence: 94.2%
Threat Score: 92
Severity: Critical
```

---

## Step 7 — Alert

The event is stored in the database.

```text
ALERT #1024

Type:
DDoS

Status:
New
```

---

## Step 8 — Dashboard

The analyst can view:

```text
Traffic
↓
Detection
↓
Alert
↓
Analytics
```

---

# 🔐 Security Considerations

The project follows a defensive security approach.

Security controls should include:

* File validation
* File-size limits
* Input validation
* Secure configuration
* Environment variables
* No secrets in source code
* Restricted CORS
* Safe error handling
* Logging
* Path traversal protection
* Authorized network monitoring

Sensitive credentials should never be stored directly inside the source code.

Use:

```text
.env
```

for local configuration.

Commit only:

```text
.env.example
```

to GitHub.

---

# ⚠️ Limitations

AI-NIDS has several limitations.

### 1. Dataset Dependency

Model performance depends heavily on the dataset used for training.

A model trained on one traffic environment may not perform identically in another environment.

### 2. False Positives

Normal unusual traffic can sometimes be classified as suspicious.

### 3. False Negatives

Some malicious traffic may not be detected.

### 4. Feature Compatibility

PCAP-derived features may not perfectly match features used by a particular public dataset.

### 5. Real-Time Performance

Real-time monitoring performance depends on:

* Hardware
* Network speed
* Packet volume
* Feature-extraction overhead
* Model complexity

### 6. Model Drift

Network behavior changes over time.

Therefore, models may require periodic evaluation and retraining.

---

# 🚀 Future Enhancements

Possible future improvements include:

## Advanced Deep Learning

Implement:

* CNN
* LSTM
* Transformer-based models
* Autoencoders

for additional anomaly-detection research.

## Federated Learning

Train models across multiple environments without directly centralizing raw traffic data.

## Cloud Deployment

Deploy the platform using:

* AWS
* Azure
* Google Cloud

## SIEM Integration

Integrate with security platforms and log-management systems.

## Advanced Alerting

Add:

* Email notifications
* Web notifications
* Security webhook integration

## Automated Incident Response

Add carefully controlled response workflows for authorized environments.

## Threat Intelligence

Integrate trusted threat-intelligence sources to enrich alerts.

## Model Monitoring

Track:

* Model drift
* Prediction distribution
* Confidence distribution
* False-positive rate

---

# 💼 Project Use Cases

AI-NIDS can be used as a foundation for:

### 🎓 Education

Cybersecurity and AI/ML learning.

### 🔬 Research

Intrusion-detection model experiments.

### 🧪 Cybersecurity Labs

Controlled network-security laboratories.

### 🏢 Security Operations

As a prototype dashboard for analyzing network-security events.

### 📊 Data Science

Network traffic classification and anomaly analysis.

---

# 📚 Learning Outcomes

By completing this project, the developer gains practical experience in:

### Artificial Intelligence

* Supervised learning
* Classification
* Model evaluation
* Feature importance
* Explainable AI

### Cybersecurity

* Network traffic analysis
* Intrusion detection
* Security alerts
* Threat scoring
* Defensive monitoring

### Data Science

* Data cleaning
* Feature engineering
* Exploratory analysis
* Dataset handling
* Visualization

### Software Development

* REST APIs
* React applications
* Database design
* Backend architecture
* Frontend/backend integration

### DevOps

* Virtual environments
* Dependency management
* Git
* Docker
* Application deployment

---

# 📈 Model Evaluation

The project should evaluate models using:

```text
Accuracy
Precision
Recall
F1 Score
Confusion Matrix
ROC-AUC
```

For imbalanced cybersecurity datasets, accuracy alone should not be treated as sufficient evidence of model quality.

Precision, recall, F1-score, class-wise results, and the confusion matrix should also be examined.

---

# 🧩 Design Philosophy

AI-NIDS follows these principles:

### 1. Explainability

The system should provide understandable information about predictions.

### 2. Modularity

ML, network processing, backend, frontend, and database components remain separated.

### 3. Reproducibility

Training and preprocessing should be reproducible.

### 4. Security

User input and uploaded files must be validated.

### 5. Transparency

The application must not fabricate model metrics or detection results.

### 6. Defensive Use

The project focuses on detecting and analyzing suspicious traffic rather than generating or executing attacks.

---

# 🏆 Final Project Summary

**AI-Powered Network Intrusion Detection System** combines:

```text
Artificial Intelligence
        +
Machine Learning
        +
Network Security
        +
Data Science
        +
Web Development
        +
Database
        +
Visualization
```

The complete system provides an end-to-end defensive workflow:

```text
Network Traffic
       ↓
Packet Analysis
       ↓
Feature Extraction
       ↓
Machine Learning
       ↓
Intrusion Detection
       ↓
Attack Classification
       ↓
Threat Score
       ↓
Security Alert
       ↓
Database
       ↓
SOC Dashboard
```

The project demonstrates how machine learning can be integrated into a cybersecurity workflow to assist with network traffic analysis and security-event visualization.

---

# 🛡️ Ethical Use

This project is intended for:

* Authorized networks
* Personal lab environments
* Educational purposes
* Cybersecurity research
* Defensive security testing

Only analyze network traffic that you are authorized to monitor.

Do not use the system to monitor, intercept, or analyze networks without appropriate permission.

---

# 👨‍💻 Author

## Rojith PJ

**B.Tech Artificial Intelligence & Data Science**

Final-Year Student

### Areas of Interest

* Artificial Intelligence
* Machine Learning
* Cybersecurity
* Data Science
* Full-Stack Development

---

# ⭐ Project Status

```text
AI-NIDS

✓ Frontend Architecture
✓ Backend Architecture
✓ ML Pipeline
✓ Network Analysis
✓ PCAP Analysis
✓ Threat Scoring
✓ Alert Management
✓ SOC Dashboard
✓ Database
✓ API
✓ Analytics
✓ Explainable AI
✓ Testing
✓ Documentation

Status: Active Development 🚀
```

---

# 📜 License

This project can be distributed under the MIT License unless a different license is specified by the project owner.

---

## 🛡️ AI-NIDS

**Turning network traffic into intelligent security insights.**

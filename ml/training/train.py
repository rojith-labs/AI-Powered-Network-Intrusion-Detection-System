import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_MODEL_DIR = BASE_DIR / "backend" / "models"
SAVED_MODEL_DIR = BASE_DIR / "ml" / "saved_models"

os.makedirs(BACKEND_MODEL_DIR, exist_ok=True)
os.makedirs(SAVED_MODEL_DIR, exist_ok=True)

# Dataset Attack Classes
ATTACK_CLASSES = [
    "BENIGN", "DoS", "DDoS", "Port Scan", "Brute Force",
    "Botnet", "Web Attack", "Infiltration", "Other"
]

FEATURE_COLUMNS = [
    "flow_duration", "fwd_pkts_count", "bwd_pkts_count", "total_bytes",
    "packet_rate", "bytes_per_sec", "avg_pkt_size", "min_pkt_size",
    "max_pkt_size", "std_pkt_size", "fwd_pkt_len_mean", "fwd_pkt_len_std",
    "bwd_pkt_len_mean", "bwd_pkt_len_std", "syn_flag_cnt", "ack_flag_cnt",
    "fin_flag_cnt", "rst_flag_cnt", "psh_flag_cnt", "source_port",
    "destination_port", "protocol", "flow_iat_mean", "flow_iat_std"
]

def generate_synthetic_dataset(num_samples: int = 5000) -> pd.DataFrame:
    """Generates synthetic dataset following CIC-IDS2017 distribution for initialization."""
    np.random.seed(42)
    records = []

    for _ in range(num_samples):
        # 60% BENIGN, 40% Attacks
        attack_roll = np.random.rand()
        if attack_roll < 0.60:
            label = "BENIGN"
            duration = np.random.exponential(1.5)
            fwd_pkts = np.random.randint(1, 20)
            bwd_pkts = np.random.randint(1, 20)
            pkt_size_avg = np.random.uniform(60, 500)
            syn_cnt = np.random.choice([0, 1], p=[0.7, 0.3])
            ack_cnt = np.random.choice([1, 2], p=[0.2, 0.8])
            rst_cnt = 0
            dest_port = int(np.random.choice([80, 443, 53, 22, np.random.randint(1024, 65535)]))
            proto = int(np.random.choice([6, 17], p=[0.8, 0.2]))
        elif attack_roll < 0.72:
            label = "DoS"
            duration = np.random.uniform(0.1, 10.0)
            fwd_pkts = np.random.randint(50, 500)
            bwd_pkts = np.random.randint(0, 10)
            pkt_size_avg = np.random.uniform(40, 120)
            syn_cnt = np.random.randint(10, 100)
            ack_cnt = 0
            rst_cnt = np.random.randint(0, 5)
            dest_port = int(np.random.choice([80, 443, 8080]))
            proto = 6
        elif attack_roll < 0.82:
            label = "DDoS"
            duration = np.random.uniform(0.05, 5.0)
            fwd_pkts = np.random.randint(100, 1000)
            bwd_pkts = np.random.randint(0, 5)
            pkt_size_avg = np.random.uniform(30, 80)
            syn_cnt = np.random.randint(50, 200)
            ack_cnt = 0
            rst_cnt = np.random.randint(0, 10)
            dest_port = int(np.random.choice([80, 443]))
            proto = 6
        elif attack_roll < 0.90:
            label = "Port Scan"
            duration = np.random.uniform(0.001, 0.5)
            fwd_pkts = np.random.randint(1, 3)
            bwd_pkts = np.random.randint(0, 1)
            pkt_size_avg = np.random.uniform(40, 64)
            syn_cnt = 1
            ack_cnt = 0
            rst_cnt = np.random.choice([0, 1])
            dest_port = int(np.random.randint(1, 1024))
            proto = 6
        elif attack_roll < 0.96:
            label = "Brute Force"
            duration = np.random.uniform(0.1, 2.0)
            fwd_pkts = np.random.randint(10, 50)
            bwd_pkts = np.random.randint(10, 50)
            pkt_size_avg = np.random.uniform(100, 300)
            syn_cnt = 1
            ack_cnt = np.random.randint(5, 20)
            rst_cnt = np.random.randint(0, 2)
            dest_port = int(np.random.choice([22, 21, 3389, 445]))
            proto = 6
        else:
            label = "Botnet"
            duration = np.random.uniform(1.0, 30.0)
            fwd_pkts = np.random.randint(20, 100)
            bwd_pkts = np.random.randint(20, 100)
            pkt_size_avg = np.random.uniform(200, 800)
            syn_cnt = np.random.randint(1, 5)
            ack_cnt = np.random.randint(10, 50)
            rst_cnt = np.random.randint(0, 3)
            dest_port = int(np.random.choice([6667, 8080, 443]))
            proto = 6

        total_bytes = int((fwd_pkts + bwd_pkts) * pkt_size_avg)
        pkt_rate = float((fwd_pkts + bwd_pkts) / max(0.001, duration))
        bytes_sec = float(total_bytes / max(0.001, duration))

        records.append({
            "flow_duration": duration,
            "fwd_pkts_count": fwd_pkts,
            "bwd_pkts_count": bwd_pkts,
            "total_bytes": total_bytes,
            "packet_rate": pkt_rate,
            "bytes_per_sec": bytes_sec,
            "avg_pkt_size": pkt_size_avg,
            "min_pkt_size": float(max(20, pkt_size_avg * 0.5)),
            "max_pkt_size": float(pkt_size_avg * 1.5),
            "std_pkt_size": float(pkt_size_avg * 0.2),
            "fwd_pkt_len_mean": float(pkt_size_avg),
            "fwd_pkt_len_std": float(pkt_size_avg * 0.15),
            "bwd_pkt_len_mean": float(pkt_size_avg * 0.9),
            "bwd_pkt_len_std": float(pkt_size_avg * 0.1),
            "syn_flag_cnt": syn_cnt,
            "ack_flag_cnt": ack_cnt,
            "fin_flag_cnt": int(np.random.choice([0, 1], p=[0.8, 0.2])),
            "rst_flag_cnt": rst_cnt,
            "psh_flag_cnt": int(np.random.choice([0, 1], p=[0.7, 0.3])),
            "source_port": int(np.random.randint(1024, 65535)),
            "destination_port": dest_port,
            "protocol": proto,
            "flow_iat_mean": float(duration / max(1, fwd_pkts + bwd_pkts)),
            "flow_iat_std": float(duration * 0.1),
            "label": label
        })

    return pd.DataFrame(records)

def train_and_evaluate(dataset_path: str = None):
    print("=" * 60)
    print("AI-NIDS Model Training & Evaluation Pipeline")
    print("=" * 60)

    if dataset_path and os.path.exists(dataset_path):
        print(f"Loading dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path)
    else:
        print("No external dataset provided. Generating synthetic CIC-IDS2017 dataset...")
        df = generate_synthetic_dataset(num_samples=6000)

    print(f"Dataset Loaded. Total Records: {len(df)}")
    print("Class Distribution:")
    print(df["label"].value_counts())

    X = df[FEATURE_COLUMNS]
    y = df["label"]

    # Label encoding
    labels = sorted(list(y.unique()))
    label_to_idx = {lbl: idx for idx, lbl in enumerate(labels)}
    idx_to_label = {idx: lbl for idx, lbl in enumerate(labels)}
    y_encoded = y.map(label_to_idx)

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
    )

    # Scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="mlogloss"),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model = None

    for name, model in models.items():
        print(f"\nTraining {name}...")
        if name == "Random Forest" or name == "XGBoost":
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)
        else:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_proba = model.predict_proba(X_test_scaled)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        try:
            auc = roc_auc_score(y_test, y_proba, multi_class="ovr")
        except Exception:
            auc = 0.0

        print(f"[{name}] Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")

        results[name] = {
            "model_name": name,
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "roc_auc": float(auc),
            "confusion_matrix": cm,
            "model_obj": model
        }

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = model

    print(f"\nSelected Best Model: {best_model_name} (F1 Score: {best_f1:.4f})")

    # Feature Importance (for Random Forest / XGBoost)
    feature_importances = []
    if hasattr(best_model, "feature_importances_"):
        fi_vals = best_model.feature_importances_
        for feat, val in zip(FEATURE_COLUMNS, fi_vals):
            feature_importances.append({"feature": feat, "importance": float(val)})
        feature_importances.sort(key=lambda x: x["importance"], reverse=True)

    # Save artifacts
    model_payload = {
        "model": best_model,
        "scaler": scaler,
        "model_name": best_model_name,
        "feature_names": FEATURE_COLUMNS,
        "labels": labels,
        "label_to_idx": label_to_idx,
        "idx_to_label": idx_to_label,
        "metrics": {
            "accuracy": results[best_model_name]["accuracy"],
            "precision": results[best_model_name]["precision"],
            "recall": results[best_model_name]["recall"],
            "f1_score": results[best_model_name]["f1_score"],
            "roc_auc": results[best_model_name]["roc_auc"],
            "confusion_matrix": results[best_model_name]["confusion_matrix"]
        },
        "feature_importances": feature_importances,
        "trained_at": datetime.utcnow().isoformat()
    }

    # Save to both target locations
    backend_path = BACKEND_MODEL_DIR / "nids_model.joblib"
    saved_path = SAVED_MODEL_DIR / "nids_model.joblib"

    joblib.dump(model_payload, backend_path)
    joblib.dump(model_payload, saved_path)

    print(f"Model saved successfully to:\n  - {backend_path}\n  - {saved_path}")

    # Also save metrics metadata json (excluding model objects)
    meta_path = BACKEND_MODEL_DIR / "model_metrics.json"
    clean_all_models = {}
    for model_name, info in results.items():
        clean_info = {
            "model_name": info["model_name"],
            "accuracy": info["accuracy"],
            "precision": info["precision"],
            "recall": info["recall"],
            "f1_score": info["f1_score"],
            "roc_auc": info["roc_auc"],
            "confusion_matrix": info["confusion_matrix"]
        }
        clean_all_models[model_name] = clean_info

    with open(meta_path, "w") as f:
        json.dump({
            "best_model": best_model_name,
            "metrics": clean_all_models[best_model_name],
            "all_models": clean_all_models,
            "feature_importances": feature_importances,
            "trained_at": datetime.now(timezone.utc).isoformat()
        }, f, indent=2)

    return model_payload

if __name__ == "__main__":
    train_and_evaluate()

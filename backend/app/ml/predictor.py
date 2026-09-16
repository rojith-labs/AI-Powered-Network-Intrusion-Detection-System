import os
import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple, List
from app.config import settings
from app.services.risk_engine import RiskEngine

class NIDSPredictor:
    """
    ML Prediction Service for NIDS.
    Loads joblib model artifact and extracts features in standard CIC-IDS2017 schema.
    """

    _instance = None
    _model_data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NIDSPredictor, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        model_path = settings.MODEL_DIR / "nids_model.joblib"
        if not model_path.exists():
            # Check secondary path in ml/saved_models/
            alt_path = settings.MODEL_DIR.parent.parent / "ml" / "saved_models" / "nids_model.joblib"
            if alt_path.exists():
                model_path = alt_path

        if model_path.exists():
            try:
                self._model_data = joblib.load(model_path)
                print(f"[NIDSPredictor] Model loaded successfully from {model_path}")
            except Exception as e:
                print(f"[NIDSPredictor] Error loading model file {model_path}: {e}")
                self._model_data = None
        else:
            print(f"[NIDSPredictor] Warning: No trained model found at {model_path}.")
            self._model_data = None

    def reload(self):
        """Reloads the model artifact from disk."""
        self._load_model()

    @property
    def is_loaded(self) -> bool:
        return self._model_data is not None

    def get_metadata(self) -> Dict[str, Any]:
        if not self._model_data:
            return {
                "status": "Not Loaded",
                "model_name": "None",
                "metrics": None
            }
        return {
            "status": "Active",
            "model_name": self._model_data.get("model_name", "Random Forest"),
            "metrics": self._model_data.get("metrics", {}),
            "labels": self._model_data.get("labels", []),
            "feature_names": self._model_data.get("feature_names", settings.FEATURE_NAMES),
            "trained_at": self._model_data.get("trained_at", "")
        }

    def predict_flow(self, features_dict: Dict[str, Any]) -> Tuple[str, float, float, str, List[Dict[str, Any]]]:
        """
        Predicts traffic class, confidence, threat score, severity, and feature importance.
        """
        # Feature vector preparation according to schema
        feature_vector = []
        for name in settings.FEATURE_NAMES:
            val = float(features_dict.get(name, 0.0))
            feature_vector.append(val)

        X_df = pd.DataFrame([feature_vector], columns=settings.FEATURE_NAMES)

        if self._model_data and "model" in self._model_data:
            model = self._model_data["model"]
            labels = self._model_data.get("labels", ["BENIGN", "DoS", "DDoS", "Port Scan", "Brute Force", "Botnet"])
            idx_to_label = self._model_data.get("idx_to_label", {i: l for i, l in enumerate(labels)})

            try:
                # Prediction & probabilities
                if hasattr(model, "predict_proba"):
                    probas = model.predict_proba(X_df)[0]
                    max_idx = int(np.argmax(probas))
                    confidence = float(probas[max_idx])
                    prediction = str(idx_to_label.get(max_idx, labels[max_idx] if max_idx < len(labels) else "BENIGN"))
                else:
                    pred_raw = model.predict(X_df)[0]
                    prediction = str(idx_to_label.get(pred_raw, "BENIGN"))
                    confidence = 0.95
            except Exception as e:
                print(f"[NIDSPredictor] Model inference error: {e}. Falling back to rule engine.")
                prediction, confidence = self._heuristic_fallback(features_dict)
        else:
            # Heuristic fallback if model artifact not available
            prediction, confidence = self._heuristic_fallback(features_dict)

        # Calculate Threat Score & Severity using RiskEngine
        threat_score, severity = RiskEngine.calculate_threat_score(prediction, confidence, features_dict)

        # Feature importances
        feature_importance_list = self._extract_feature_importances(features_dict)

        return prediction, confidence, threat_score, severity, feature_importance_list

    def _heuristic_fallback(self, f: Dict[str, Any]) -> Tuple[str, float]:
        """Rule-based heuristic fallback if ML model is missing."""
        pkt_rate = float(f.get("packet_rate", 0))
        syn_cnt = int(f.get("syn_flag_cnt", 0))
        ack_cnt = int(f.get("ack_flag_cnt", 0))
        dst_port = int(f.get("destination_port", 0))
        duration = float(f.get("flow_duration", 0))

        if pkt_rate > 1000 and syn_cnt > 50 and ack_cnt == 0:
            return "DDoS", 0.94
        elif pkt_rate > 300 and syn_cnt > 20:
            return "DoS", 0.88
        elif duration < 0.1 and syn_cnt == 1 and ack_cnt == 0 and dst_port < 1024:
            return "Port Scan", 0.85
        elif dst_port in [22, 21, 3389, 445] and pkt_rate > 20:
            return "Brute Force", 0.82
        elif dst_port in [6667, 8080] and float(f.get("total_bytes", 0)) > 50000:
            return "Botnet", 0.79
        else:
            return "BENIGN", 0.96

    def _extract_feature_importances(self, features_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extracts top relevant feature contributions for explainability."""
        importances = []
        if self._model_data and "feature_importances" in self._model_data:
            fi_data = self._model_data["feature_importances"]
            for item in fi_data[:8]: # Top 8 features
                feat_name = item["feature"]
                val = float(features_dict.get(feat_name, 0.0))
                importances.append({
                    "feature": feat_name,
                    "value": round(val, 2),
                    "importance": round(item["importance"], 4),
                    "description": f"{feat_name.replace('_', ' ').title()}: {val:.2f}"
                })
        else:
            # Default fallback importances
            default_feats = ["packet_rate", "syn_flag_cnt", "total_bytes", "flow_duration", "destination_port"]
            for feat in default_feats:
                val = float(features_dict.get(feat, 0.0))
                importances.append({
                    "feature": feat,
                    "value": round(val, 2),
                    "importance": 0.2,
                    "description": f"{feat.replace('_', ' ').title()}: {val:.2f}"
                })
        return importances

predictor = NIDSPredictor()

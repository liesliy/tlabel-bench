#!/usr/bin/env python3
"""
material_classification.py — Material classification benchmark for TLabel-Bench.

Evaluates how well TLabel features can classify objects by material category
(rigid / soft / deformable) across different sensors.

Usage:
    python evaluation/material_classification.py [--sensor SENSOR] [--kfold 5]

Metrics:
    - Accuracy
    - Macro F1 Score
    - Per-class Precision/Recall
"""

import argparse
import json
from pathlib import Path
from collections import defaultdict

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    from sklearn.metrics import classification_report, f1_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("Warning: scikit-learn not installed. Run: pip install scikit-learn")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

ANNOTATIONS_DIR = Path(__file__).parent.parent / "annotations"


def load_features_and_labels(sensor: str):
    """Load TLabel features and material labels for a sensor."""
    ann_path = ANNOTATIONS_DIR / sensor / "annotations.json"
    if not ann_path.exists():
        return None, None

    with open(ann_path, "r") as f:
        data = json.load(f)

    X, y = [], []
    for ann in data.get("annotations", []):
        features = ann.get("features", {})
        if not features:
            continue
        feature_vector = [
            features.get("eccentricity", 0),
            features.get("skewness", 0),
            features.get("kurtosis", 0),
            features.get("contact_ratio", 0),
            features.get("slip_entropy", 0),
            features.get("pressure_variance", 0),
        ]
        X.append(feature_vector)
        y.append(ann["material_label"])

    return np.array(X) if X else None, np.array(y) if y else None


def evaluate_sensor(sensor: str, kfold: int = 5) -> dict:
    """Run material classification evaluation for a single sensor."""
    if not HAS_SKLEARN or not HAS_NUMPY:
        return {"sensor": sensor, "error": "Missing dependencies"}

    X, y = load_features_and_labels(sensor)
    if X is None or len(X) < kfold:
        return {"sensor": sensor, "error": "Insufficient data", "n_samples": 0 if X is None else len(X)}

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    skf = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=42)

    accuracies = cross_val_score(clf, X, y, cv=skf, scoring="accuracy")
    f1_scores = cross_val_score(clf, X, y, cv=skf, scoring="f1_macro")

    return {
        "sensor": sensor,
        "n_samples": len(X),
        "n_classes": len(set(y)),
        "accuracy_mean": round(float(accuracies.mean()), 4),
        "accuracy_std": round(float(accuracies.std()), 4),
        "f1_macro_mean": round(float(f1_scores.mean()), 4),
        "f1_macro_std": round(float(f1_scores.std()), 4),
    }


def main():
    parser = argparse.ArgumentParser(description="TLabel-Bench Material Classification Evaluation")
    parser.add_argument("--sensor", default="all", help="Sensor to evaluate (all/gelsight/digit/dma/xense)")
    parser.add_argument("--kfold", type=int, default=5, help="Number of CV folds")
    args = parser.parse_args()

    sensors = [d.name for d in ANNOTATIONS_DIR.iterdir() if d.is_dir()] if args.sensor == "all" else [args.sensor]

    print("TLabel-Bench: Material Classification Evaluation")
    print("=" * 55)

    for sensor in sensors:
        result = evaluate_sensor(sensor, args.kfold)
        if "error" in result:
            print(f"\n❌ {sensor}: {result['error']}")
        else:
            print(f"\n✅ {sensor}:")
            print(f"   Samples: {result['n_samples']} | Classes: {result['n_classes']}")
            print(f"   Accuracy: {result['accuracy_mean']:.4f} ± {result['accuracy_std']:.4f}")
            print(f"   F1 (macro): {result['f1_macro_mean']:.4f} ± {result['f1_macro_std']:.4f}")


if __name__ == "__main__":
    main()

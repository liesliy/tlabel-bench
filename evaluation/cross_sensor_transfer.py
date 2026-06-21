#!/usr/bin/env python3
"""
cross_sensor_transfer.py — Cross-sensor transfer evaluation for TLabel-Bench.

Evaluates how well a model trained on one sensor transfers to another.
This is the core experiment that demonstrates TLabel's sensor-agnostic value.

Protocol:
    1. Train material classifier on sensor A
    2. Test on sensor B (zero-shot, using same TLabel features)
    3. Compare with within-sensor baseline

Usage:
    python evaluation/cross_sensor_transfer.py
"""

import json
from pathlib import Path
from itertools import permutations

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, f1_score
    import numpy as np
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

ANNOTATIONS_DIR = Path(__file__).parent.parent / "annotations"


def load_sensor_data(sensor: str):
    """Load features and labels for a sensor."""
    ann_path = ANNOTATIONS_DIR / sensor / "annotations.json"
    if not ann_path.exists():
        return None, None

    with open(ann_path, "r") as f:
        data = json.load(f)

    X, y, obj_ids = [], [], []
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
        obj_ids.append(ann["object_id"])

    return (np.array(X), np.array(y), set(obj_ids)) if X else (None, None, None)


def main():
    print("TLabel-Bench: Cross-Sensor Transfer Evaluation")
    print("=" * 50)

    if not HAS_DEPS:
        print("Missing dependencies. Run: pip install scikit-learn numpy")
        return

    sensors = [d.name for d in ANNOTATIONS_DIR.iterdir() if d.is_dir()]
    sensor_data = {}
    for s in sensors:
        X, y, obj_ids = load_sensor_data(s)
        if X is not None:
            sensor_data[s] = (X, y, obj_ids)
            print(f"  {s}: {len(X)} samples, {len(obj_ids)} objects")

    if len(sensor_data) < 2:
        print("\nNeed at least 2 sensors with data for transfer evaluation")
        return

    # Cross-sensor transfer matrix
    print(f"\n{'Train ↓ / Test →':<20}", end="")
    for s in sensors:
        if s in sensor_data:
            print(f"{s:<15}", end="")
    print()

    for train_sensor in sensors:
        if train_sensor not in sensor_data:
            continue
        X_train, y_train, train_objs = sensor_data[train_sensor]
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        print(f"{train_sensor:<20}", end="")

        for test_sensor in sensors:
            if test_sensor not in sensor_data:
                continue
            X_test, y_test, test_objs = sensor_data[test_sensor]

            if train_sensor == test_sensor:
                # Within-sensor baseline (train on 80%, test on 20%)
                from sklearn.model_selection import cross_val_score
                scores = cross_val_score(clf, X_train, y_train, cv=min(5, len(X_train)), scoring="accuracy")
                print(f"{scores.mean():.3f}±{scores.std():.2f}  ", end="")
            else:
                # Cross-sensor zero-shot
                # Only test on common objects for fair comparison
                common = train_objs & test_objs
                if common:
                    mask = np.array([oid in common for oid in [ann.get("object_id", "") for ann in
                        json.load(open(ANNOTATIONS_DIR / test_sensor / "annotations.json")).get("annotations", [])]])
                    if mask.any():
                        y_pred = clf.predict(X_test[mask] if len(mask) == len(X_test) else X_test)
                        acc = accuracy_score(y_test, y_pred) if len(y_test) == len(y_pred) else 0.0
                        print(f"{acc:.3f}          ", end="")
                    else:
                        print(f"{'N/A':<15}", end="")
                else:
                    print(f"{'N/A':<15}", end="")
        print()

    print("\nNote: Values show accuracy. Within-sensor = CV baseline, Cross-sensor = zero-shot transfer.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
verify_data.py — Verify integrity of TLabel-Bench data.

Checks:
1. Annotation files conform to schema
2. All required fields are present
3. Quality scores are within valid range
4. Episode segmentation is logically consistent
5. Object IDs are consistent across sensors

Usage:
    python scripts/verify_data.py
"""

import json
from pathlib import Path
from collections import defaultdict

ANNOTATIONS_DIR = Path(__file__).parent.parent / "annotations"

REQUIRED_FIELDS = ["object_id", "material_label", "interaction_id", "episode", "quality_score", "quality_level"]
VALID_MATERIALS = {"rigid", "soft", "deformable"}
VALID_QUALITY_LEVELS = {"excellent", "good", "acceptable", "poor"}


def verify_annotation_file(sensor: str) -> dict:
    """Verify a single sensor's annotation file."""
    ann_path = ANNOTATIONS_DIR / sensor / "annotations.json"
    result = {"sensor": sensor, "valid": True, "errors": [], "stats": {}}

    if not ann_path.exists():
        result["valid"] = False
        result["errors"].append(f"Annotation file not found: {ann_path}")
        return result

    with open(ann_path, "r") as f:
        data = json.load(f)

    annotations = data.get("annotations", [])
    result["stats"]["total_annotations"] = len(annotations)
    result["stats"]["unique_objects"] = len(set(a["object_id"] for a in annotations if "object_id" in a))

    for i, ann in enumerate(annotations):
        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in ann:
                result["errors"].append(f"Annotation {i}: missing field '{field}'")
                result["valid"] = False

        # Check material label
        if ann.get("material_label") not in VALID_MATERIALS:
            result["errors"].append(f"Annotation {i}: invalid material_label '{ann.get('material_label')}'")
            result["valid"] = False

        # Check quality score range
        qs = ann.get("quality_score")
        if qs is not None and (qs < 0.0 or qs > 1.0):
            result["errors"].append(f"Annotation {i}: quality_score {qs} out of range [0, 1]")
            result["valid"] = False

        # Check quality level
        if ann.get("quality_level") not in VALID_QUALITY_LEVELS:
            result["errors"].append(f"Annotation {i}: invalid quality_level '{ann.get('quality_level')}'")
            result["valid"] = False

        # Check episode segmentation
        episode = ann.get("episode", {})
        for phase in ["contact", "press", "release"]:
            if phase not in episode:
                result["errors"].append(f"Annotation {i}: missing episode phase '{phase}'")
                result["valid"] = False
            else:
                if episode[phase].get("start_frame", -1) > episode[phase].get("end_frame", -1):
                    result["errors"].append(f"Annotation {i}: {phase} start_frame > end_frame")
                    result["valid"] = False

    return result


def check_cross_sensor_consistency():
    """Check that object IDs are consistent across sensors."""
    sensor_objects = {}
    for sensor_dir in ANNOTATIONS_DIR.iterdir():
        if not sensor_dir.is_dir():
            continue
        ann_path = sensor_dir / "annotations.json"
        if not ann_path.exists():
            continue
        with open(ann_path, "r") as f:
            data = json.load(f)
        objects = set(a["object_id"] for a in data.get("annotations", []) if "object_id" in a)
        sensor_objects[sensor_dir.name] = objects

    if len(sensor_objects) < 2:
        return {"consistent": True, "message": "Need at least 2 sensors to check consistency"}

    all_objects = set.union(*sensor_objects.values())
    common_objects = set.intersection(*sensor_objects.values())

    return {
        "consistent": len(common_objects) > 0,
        "total_unique_objects": len(all_objects),
        "common_objects": len(common_objects),
        "common_object_ids": sorted(common_objects)[:20],  # First 20
        "per_sensor": {s: len(objs) for s, objs in sensor_objects.items()},
    }


def main():
    print("TLabel-Bench Data Verification")
    print("=" * 40)

    sensors = [d.name for d in ANNOTATIONS_DIR.iterdir() if d.is_dir()]

    all_valid = True
    for sensor in sensors:
        result = verify_annotation_file(sensor)
        status = "✅ PASS" if result["valid"] else "❌ FAIL"
        print(f"\n{status} {sensor}: {result['stats'].get('total_annotations', 0)} annotations, "
              f"{result['stats'].get('unique_objects', 0)} objects")
        for err in result["errors"][:5]:
            print(f"  ⚠️ {err}")
        if not result["valid"]:
            all_valid = False

    print("\n" + "-" * 40)
    print("Cross-Sensor Consistency:")
    consistency = check_cross_sensor_consistency()
    if consistency.get("consistent"):
        print(f"  ✅ {consistency['common_objects']} common objects across sensors")
    else:
        print("  ⚠️ No common objects found across sensors")

    print(f"\nOverall: {'✅ ALL VALID' if all_valid else '❌ ISSUES FOUND'}")


if __name__ == "__main__":
    main()

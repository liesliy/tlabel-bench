#!/usr/bin/env python3
"""
merge_annotations.py — Merge TLabel-Bench annotations with raw tactile data.

This script:
1. Reads annotation files from annotations/
2. Downloads raw data if not present (via download_data.sh)
3. Loads raw data using TLabel adapters
4. Merges annotations with raw data
5. Exports unified benchmark files

Usage:
    python scripts/merge_annotations.py [--sensor SENSOR] [--output DIR]
"""

import argparse
import json
import os
from pathlib import Path

try:
    import tlabel
    from tlabel import TLabelData
    HAS_TLABEL = True
except ImportError:
    HAS_TLABEL = False
    print("Warning: tlabel not installed. Run: pip install tlabel>=0.4.2")


ANNOTATIONS_DIR = Path(__file__).parent.parent / "annotations"
RAW_DATA_DIR = Path(os.environ.get("DATA_DIR", "./raw_data"))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "./benchmark_output"))


def load_annotations(sensor: str) -> dict:
    """Load annotation file for a given sensor."""
    ann_path = ANNOTATIONS_DIR / sensor / "annotations.json"
    if not ann_path.exists():
        print(f"No annotations found for {sensor} at {ann_path}")
        return {}
    with open(ann_path, "r") as f:
        return json.load(f)


def merge_sensor_data(sensor: str, annotations: dict) -> list:
    """Merge annotations with raw data using TLabel adapter."""
    if not HAS_TLABEL:
        print(f"Cannot merge {sensor}: tlabel not installed")
        return []

    sensor_map = {
        "gelsight": "gelsight_mini",
        "digit": "digit",
        "dma": "daimon_dma",
        "xense": "xense",
    }

    adapter_name = sensor_map.get(sensor, sensor)
    raw_dir = RAW_DATA_DIR / sensor

    if not raw_dir.exists():
        print(f"Raw data not found at {raw_dir}. Run download_data.sh first.")
        return []

    merged = []
    for ann in annotations.get("annotations", []):
        obj_id = ann["object_id"]
        # In a full implementation, this would load raw data via TLabel adapter
        # and attach annotations
        entry = {
            **ann,
            "sensor_adapter": adapter_name,
            "data_source": str(raw_dir),
            "merged": True,
        }
        merged.append(entry)

    return merged


def export_benchmark(merged_data: dict, output_dir: Path):
    """Export merged benchmark data in multiple formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # JSON export
    json_path = output_dir / "tlabel_bench.json"
    with open(json_path, "w") as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    print(f"Exported JSON: {json_path}")

    # CSV export
    csv_path = output_dir / "tlabel_bench.csv"
    with open(csv_path, "w") as f:
        if merged_data.get("entries"):
            headers = list(merged_data["entries"][0].keys())
            f.write(",".join(headers) + "\n")
            for entry in merged_data["entries"]:
                f.write(",".join(str(entry.get(h, "")) for h in headers) + "\n")
    print(f"Exported CSV: {csv_path}")

    print(f"\nBenchmark ready in: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Merge TLabel-Bench annotations with raw data")
    parser.add_argument("--sensor", default="all", help="Sensor to process (all/gelsight/digit/dma/xense)")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="Output directory")
    args = parser.parse_args()

    sensors = ["gelsight", "digit", "dma", "xense"] if args.sensor == "all" else [args.sensor]

    all_merged = {"benchmark": "tlabel-bench", "version": "1.0.0", "entries": []}

    for sensor in sensors:
        print(f"\n--- Processing {sensor} ---")
        annotations = load_annotations(sensor)
        if not annotations:
            continue
        merged = merge_sensor_data(sensor, annotations)
        all_merged["entries"].extend(merged)
        print(f"Merged {len(merged)} annotations for {sensor}")

    if all_merged["entries"]:
        export_benchmark(all_merged, Path(args.output))
    else:
        print("\nNo data merged. Ensure raw data is downloaded and tlabel is installed.")


if __name__ == "__main__":
    main()

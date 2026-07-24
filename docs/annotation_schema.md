# Annotation Schema

This document defines the JSON schema for TLabel-Bench annotation files.

**TLabel Version:** 0.17+ (Schema V2)  
**Last Updated:** 2026-07-24

---

## Top-Level Structure

```json
{
  "benchmark": "tlabel-bench",
  "version": "1.0.0",
  "sensor_type": "gelsight_mini",
  "generated_with": "tlabel>=0.17.0",
  "schema_version": "v2",
  "annotations": [...]
}
```

## Annotation Object

Each annotation in the `annotations` array has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `object_id` | string | ✅ | Unique identifier for the object (e.g., "obj_001") |
| `material_label` | string | ✅ | Material category: "rigid", "soft", or "deformable" |
| `material_detail` | string | ❌ | Fine-grained material description (e.g., "aluminum", "rubber") |
| `interaction_id` | integer | ✅ | Interaction number for this object (1-based) |
| `episode` | object | ✅ | Episode segmentation (see below) |
| `quality_score` | float | ✅ | Data quality score, range [0.0, 1.0] |
| `quality_level` | string | ✅ | "excellent" (≥0.8), "good" (≥0.6), "acceptable" (≥0.4), "poor" (<0.4) |
| `features` | object | ❌ | Pre-computed features from 14-dim Schema V2 (see below) |
| `notes` | string | ❌ | Free-text notes from annotator |

## Episode Segmentation

```json
{
  "contact": {
    "start_frame": 0,
    "end_frame": 45
  },
  "press": {
    "start_frame": 46,
    "end_frame": 180
  },
  "release": {
    "start_frame": 181,
    "end_frame": 220
  }
}
```

| Phase | Description |
|-------|-------------|
| `contact` | Initial contact between sensor and object surface |
| `press` | Sustained pressure / manipulation phase |
| `release` | Sensor lifting off the object surface |

## Quality Score

Computed by TLabel's quality scoring module (v0.4+):

| Score Range | Level | Interpretation |
|-------------|-------|----------------|
| 0.8 – 1.0 | excellent | Clean signal, minimal noise, clear features |
| 0.6 – 0.8 | good | Usable with minor quality issues |
| 0.4 – 0.6 | acceptable | Significant noise but still informative |
| < 0.4 | poor | Consider excluding from analysis |

## TLabel Features (Optional)

When pre-computed features are included, they are derived from the 14-dimensional TLabel Schema V2:

```json
{
  "features": {
    "contact": 1.0,
    "force_magnitude": 0.45,
    "slip_event": 0.0,
    "object_deformation": 0.12,
    "temperature": 25.3,
    "confidence": 0.95
  }
}
```

The 14 Schema V2 dimensions are:

| # | Field | Type | Required |
|---|-------|------|----------|
| 1 | `contact` | bool | Required |
| 2 | `contact_centroid` | [float, float] | Required (if contact) |
| 3 | `contact_region` | enum | Optional |
| 4 | `force_magnitude` | float | Required (L2+) |
| 5 | `force_vector` | [float×3] | Optional (L3+) |
| 6 | `torque_vector` | [float×3] | Optional |
| 7 | `slip_event` | bool | Required |
| 8 | `slip_velocity` | [float, float] | Optional (if slip) |
| 9 | `manipulation_phase` | enum | Optional |
| 10 | `texture_class` | enum | Optional |
| 11 | `object_deformation` | float | Optional |
| 12 | `temperature` | float | Optional |
| 13 | `confidence` | float | Required |
| 14 | `compliance_level` | enum (L1/L2/L3/L4) | Required |

These features are sensor-agnostic — the same 14-dimensional schema is used regardless of sensor type, enabling direct cross-sensor comparison.

---

## Export Formats

TLabel-Bench annotations are available in three formats:

| Format | File | Use Case |
|--------|------|----------|
| JSON | `annotations.json` | Human-readable, web applications |
| CSV | `annotations.csv` | Spreadsheet analysis, quick inspection |
| HDF5 | `annotations.h5` | Large-scale ML training, efficient I/O |

All three formats contain identical information, just differently structured.

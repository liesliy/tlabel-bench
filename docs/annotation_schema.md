# Annotation Schema

This document defines the JSON schema for TLabel-Bench annotation files.

---

## Top-Level Structure

```json
{
  "benchmark": "tlabel-bench",
  "version": "1.0.0",
  "sensor_type": "gelsight_mini",
  "generated_with": "tlabel>=0.4.2",
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
| `features` | object | ❌ | Pre-computed TLabel features (see below) |
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

When pre-computed features are included:

```json
{
  "features": {
    "eccentricity": 0.82,
    "skewness": -0.15,
    "kurtosis": 2.93,
    "contact_ratio": 0.71,
    "slip_entropy": 0.34,
    "pressure_variance": 0.028
  }
}
```

These features are sensor-agnostic — the same 18-dimensional feature vector is computed regardless of sensor type, enabling direct cross-sensor comparison.

---

## Export Formats

TLabel-Bench annotations are available in three formats:

| Format | File | Use Case |
|--------|------|----------|
| JSON | `annotations.json` | Human-readable, web applications |
| CSV | `annotations.csv` | Spreadsheet analysis, quick inspection |
| HDF5 | `annotations.h5` | Large-scale ML training, efficient I/O |

All three formats contain identical information, just differently structured.

<h1 align="center">🦞 TLabel-Bench</h1>

<p align="center">
  <strong>The First Cross-Sensor Unified Tactile Annotation Benchmark</strong>
</p>

<p align="center">
  <a href="https://github.com/liesliy/tlabel"><img src="https://img.shields.io/badge/Powered%20by-TLabel-blue" alt="TLabel"></a>
  <a href="https://github.com/liesliy/tlabel-bench/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-green" alt="License"></a>
  <img src="https://img.shields.io/badge/Sensors-GelSight%20%7C%20DIGIT%20%7C%20DMA%20%7C%20Xense-orange" alt="Sensors">
</p>

---

## 🎯 Why TLabel-Bench?

Every public tactile dataset today is **sensor-specific** — GelSight data only has GelSight format, DIGIT only DIGIT, DMA only DMA. **No one has ever annotated the same set of objects across different sensors in a unified format that enables direct comparison.**

TLabel-Bench fills this gap. It is the first benchmark that provides:

- **Cross-sensor annotations** for the same objects across GelSight Mini, DIGIT, DMA, and Xense
- **Unified TLabel format** — switch sensors by switching adapters, labels stay identical
- **Multi-level annotations** — material labels, episode segmentation (contact → press → release), and quality scores
- **Three export formats** — HDF5, CSV, and JSON for maximum compatibility

---

## 📦 What's Included

```
tlabel-bench/
├── annotations/           ← TLabel annotation files (JSON/CSV)
│   ├── gelsight/          ← GelSight Mini annotations
│   ├── digit/             ← DIGIT annotations
│   ├── dma/               ← DMA (Daimon) annotations
│   └── xense/             ← Xense annotations
├── scripts/               ← Auto-download & merge scripts
├── evaluation/            ← Benchmark evaluation scripts
├── docs/                  ← Documentation
└── examples/              ← Quickstart notebooks
```

**Note:** This repository only contains annotation files and scripts. Raw sensor data must be downloaded separately using the provided scripts (see [Data Sources](docs/data_sources.md)).

---

## 🚀 Quick Start

### 1. Install TLabel

```bash
pip install tlabel>=0.4.2
```

### 2. Download raw data

```bash
bash scripts/download_data.sh
```

### 3. Merge annotations with raw data

```bash
python scripts/merge_annotations.py
```

### 4. Run evaluation

```bash
python evaluation/material_classification.py
```

---

## 📊 Annotation Schema

Each annotation file follows the TLabel standard schema:

| Field | Type | Description |
|-------|------|-------------|
| `sensor_type` | string | Sensor adapter name (e.g., "gelsight_mini") |
| `object_id` | string | Unique object identifier |
| `material_label` | string | Material category (rigid, soft, deformable) |
| `episode` | object | Episode segmentation: contact, press, release |
| `quality_score` | float | Data quality score (0.0–1.0) |
| `timestamp` | float | Relative timestamp in seconds |

See [annotation_schema.md](docs/annotation_schema.md) for the full specification.

---

## 🔬 Evaluation Tasks

| Task | Metric | Description |
|------|--------|-------------|
| Material Classification | Accuracy / F1 | Classify objects by material using TLabel features |
| Episode Segmentation | IoU / F1 | Detect contact→press→release boundaries |
| Cross-Sensor Transfer | Accuracy drop | Train on sensor A, test on sensor B |
| Quality Assessment | Correlation | Predict human quality ratings |

---

## ⚖️ Legal & Data Sources

This repository contains **only annotation files** (labels and metadata). Raw tactile data must be downloaded from their original sources. See [data_sources.md](docs/data_sources.md) for:

- Download links for each dataset
- License information
- Citation requirements

**Why only annotations?** Many tactile datasets do not have permissive licenses for redistribution. Our annotation files are original works under CC-BY-4.0, while raw data remains subject to their respective licenses.

---

## 🔗 Related Projects

- **[TLabel](https://github.com/liesliy/tlabel)** — Sensor-agnostic tactile annotation toolkit (the tool that generates these annotations)
- **[Touch and Go](https://sites.google.com/view/touch-and-go)** — GelSight tactile-visual dataset
- **[SSVTP](https://github.com/CMURoboTouch/SSVTP)** — DIGIT-based tactile pose estimation
- **[ObjTac](https://github.com/zhuochen10/ObjTac)** — Multi-object tactile dataset

---

## 📝 Citation

If you use TLabel-Bench in your research, please cite:

```bibtex
@dataset{tlabel_bench_2026,
  title={TLabel-Bench: The First Cross-Sensor Unified Tactile Annotation Benchmark},
  author={Wu, Sheng and Luo, Xi},
  year={2026},
  publisher={GitHub},
  url={https://github.com/liesliy/tlabel-bench}
}
```

---

## 🤝 Contributing

We welcome contributions! See [contribute.md](docs/contribute.md) for guidelines.

Areas we especially need help with:
- New sensor adapters (SynTouch, XELA, etc.)
- Additional objects and annotations
- Evaluation metrics and baselines

---

## 📄 License

Annotation files are licensed under [CC-BY-4.0](LICENSE). Raw data is subject to their respective original licenses.

---

<p align="center">
  Built with 🦞 by <a href="https://github.com/liesliy">NiuXu Technology</a>
</p>

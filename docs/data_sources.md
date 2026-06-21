# Data Sources & License Information

This document lists the original tactile datasets used to generate TLabel-Bench annotations, along with their download links and license status.

## Important Notice

**This repository does NOT contain any raw tactile data.** All raw data must be downloaded from their original sources. The annotation files in this repository are original works under CC-BY-4.0.

---

## Dataset Summary

| Dataset | Sensor | Objects | License | Status |
|---------|--------|---------|---------|--------|
| Touch and Go | GelSight Mini | ~100 | Not specified (ARR) | Annotations only |
| SSVTP | DIGIT | ~50 | Not specified (ARR) | Annotations only |
| ObjTac | PaXini DMA | ~30 | Not specified (ARR) | Annotations only |
| Daimon-Infinity (samples) | DMA HD | Partial | CC-BY-NC-SA-4.0 | Annotations only |

> **ARR** = All Rights Reserved (default when no license is specified). This means the raw data cannot be redistributed. Our annotation files are independent creative works.

---

## 1. Touch and Go

- **Sensor:** GelSight Mini
- **Paper:** "Touch and Go: Learning to Grasp with Tactile Signals" (ICRA 2024)
- **Download:** Follow instructions at the project website
- **License:** Not specified — All Rights Reserved
- **Usage in TLabel-Bench:** We extract GelSight Mini tactile frames and provide material labels, episode annotations, and quality scores. No raw data is redistributed.

## 2. SSVTP (Self-Supervised Visuo-Tactile Pre-training)

- **Sensor:** DIGIT
- **Paper:** "Self-Supervised Visuo-Tactile Pre-training for Robotic Manipulation" (CoRL 2023)
- **Source:** CMU RoboTouch
- **License:** Not specified — All Rights Reserved
- **Usage in TLabel-Bench:** We extract DIGIT tactile frames and provide cross-sensor comparable annotations.

## 3. ObjTac

- **Sensor:** PaXini DMA (Multi-zone tactile sensor)
- **Paper:** "ObjTac: Multi-Object Tactile Dataset for Robotic Manipulation" (2024)
- **Authors:** Zhuo Chen et al., King's College London
- **License:** Not specified — All Rights Reserved
- **Usage in TLabel-Bench:** We provide TLabel annotations compatible with our existing ObjTac×TLabel T4/T5 experiment results.

## 4. Daimon-Infinity (Samples)

- **Sensor:** DMA High-Resolution Tactile Sensor
- **Source:** Daimon Robotics / ModelScope
- **License:** CC-BY-NC-SA-4.0
- **Note:** Non-commercial use only. Our annotations can be used commercially (CC-BY-4.0), but the raw data under this license cannot.
- **Usage in TLabel-Bench:** We use publicly available sample data to demonstrate DMA sensor compatibility.

---

## Self-Collected Data

Any self-collected DMA data (100% owned by NiuXu Technology) can be included directly in this repository with full licensing freedom. This data will be clearly marked as "NiuXu proprietary" and released under CC-BY-4.0.

---

## Legal Boundary

| What | License | Can redistribute? |
|------|---------|-------------------|
| TLabel annotation files (JSON/CSV) | CC-BY-4.0 | ✅ Yes |
| Download scripts | MIT | ✅ Yes |
| Raw tactile data | Respective original licenses | ❌ No |
| Self-collected data | CC-BY-4.0 | ✅ Yes |

If you are a dataset owner and believe your data should not be referenced here, please open an issue or contact us.

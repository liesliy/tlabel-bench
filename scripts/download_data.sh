#!/bin/bash
# download_data.sh — Download raw tactile datasets for TLabel-Bench
# 
# IMPORTANT: Each dataset is subject to its own license terms.
# See docs/data_sources.md for license information.
#
# Usage:
#   bash scripts/download_data.sh              # Download all
#   bash scripts/download_data.sh gelsight     # Download only GelSight data
#   bash scripts/download_data.sh digit        # Download only DIGIT data
#   bash scripts/download_data.sh dma          # Download only DMA data

set -e

DATA_DIR="${DATA_DIR:-./raw_data}"
mkdir -p "$DATA_DIR"

download_gelsight() {
    echo "=== Downloading Touch and Go (GelSight Mini) ==="
    echo "Source: Touch and Go project page"
    echo "License: Not specified (All Rights Reserved)"
    echo ""
    echo "Please follow the instructions at the project website to download."
    echo "After downloading, place the data in: $DATA_DIR/touch_and_go/"
    echo ""
    mkdir -p "$DATA_DIR/touch_and_go"
    echo "[placeholder] Actual download requires manual steps per dataset policy."
}

download_digit() {
    echo "=== Downloading SSVTP (DIGIT) ==="
    echo "Source: CMU RoboTouch / SSVTP project"
    echo "License: Not specified (All Rights Reserved)"
    echo ""
    echo "Please follow the instructions at the project website to download."
    echo "After downloading, place the data in: $DATA_DIR/ssvtp/"
    echo ""
    mkdir -p "$DATA_DIR/ssvtp"
    echo "[placeholder] Actual download requires manual steps per dataset policy."
}

download_dma() {
    echo "=== Downloading DMA Data ==="
    echo ""
    echo "1. ObjTac (PaXini DMA):"
    echo "   Source: KCL Zhuo Chen lab"
    echo "   License: Not specified (All Rights Reserved)"
    echo "   Place in: $DATA_DIR/objtac/"
    mkdir -p "$DATA_DIR/objtac"
    echo ""
    echo "2. Daimon-Infinity Samples (DMA HD):"
    echo "   Source: ModelScope (Daimon Robotics)"
    echo "   License: CC-BY-NC-SA-4.0 (Non-commercial only)"
    echo "   Place in: $DATA_DIR/daimon_infinity/"
    mkdir -p "$DATA_DIR/daimon_infinity"
    echo ""
    echo "[placeholder] Actual download requires manual steps per dataset policy."
}

# Main
TARGET="${1:-all}"

case "$TARGET" in
    all)
        download_gelsight
        download_digit
        download_dma
        ;;
    gelsight)
        download_gelsight
        ;;
    digit)
        download_digit
        ;;
    dma)
        download_dma
        ;;
    *)
        echo "Unknown dataset: $TARGET"
        echo "Usage: bash scripts/download_data.sh [all|gelsight|digit|dma]"
        exit 1
        ;;
esac

echo ""
echo "=== Download script complete ==="
echo "Raw data directory: $DATA_DIR"
echo ""
echo "Next step: python scripts/merge_annotations.py"

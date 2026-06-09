#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

out_dir="live_demo/output/publications_stufe_only"
mkdir -p "$out_dir"

python main.py live_demo/dsl_scripts/publications_stufe_only.dsl \
    --data-dir live_demo/data \
    --backend graphviz \
    --dot-output "$out_dir/publications_stufe_only.dot" \
    --output "$out_dir/publications_stufe_only.png"

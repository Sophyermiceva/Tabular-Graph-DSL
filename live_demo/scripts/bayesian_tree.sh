#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

out_dir="live_demo/output/bayesian_tree"
mkdir -p "$out_dir"

python main.py live_demo/dsl_scripts/bayesian_tree.dsl \
    --data-dir live_demo/data \
    --backend bayes \
    --dot-output "$out_dir/bayesian_tree.dot" \
    --output "$out_dir/bayesian_tree.png"

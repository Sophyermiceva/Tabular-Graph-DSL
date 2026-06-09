#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

out_dir="live_demo/output/build_graph_graphviz"
mkdir -p "$out_dir"

python main.py live_demo/dsl_scripts/build_graph.dsl \
    --data-dir live_demo/data \
    --backend graphviz \
    --dot-output "$out_dir/build_graph.dot" \
    --output "$out_dir/build_graph.png"

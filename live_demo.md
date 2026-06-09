# Live Demo Commands

Run these commands from the project root:

```bash
cd /home/alderson/Projects/Mine/labs/elsd/project
```

The shell scripts live in `live_demo/scripts`, the DSL files live in
`live_demo/dsl_scripts`, CSV files live in `live_demo/data`, and generated files
go under `live_demo/output`. Each shell script creates its own output
subdirectory before running, so output paths will not fail with a
missing-directory error.

## 1. Basic Graph With Graphviz Backend

Generates DOT and PNG output for the user/product purchase graph.

```bash
bash live_demo/scripts/build_graph_graphviz.sh
```

## 2. Basic Graph With NetworkX Backend

Runs the interpreter path that builds a Python `networkx.DiGraph`, then renders it
with the matplotlib visualizer.

```bash
bash live_demo/scripts/build_graph_networkx.sh
```

## 3. Bayesian Tree Backend

Runs the Bayesian backend, prints computed probabilities, saves DOT, and renders
the tree as an image.

```bash
bash live_demo/scripts/bayesian_tree.sh
```

## 4. Publications Stufe Graph With Graphviz Backend

Renders `publications.csv` while displaying only `Stufe 1`, `Stufe 2`, and
`Stufe 3` nodes.

```bash
bash live_demo/scripts/publications_stufe_only.sh
```

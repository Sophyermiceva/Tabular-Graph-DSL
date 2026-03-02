"""Graph visualizer using matplotlib and networkx."""

from typing import Optional, Dict, List, Tuple

import networkx as nx
import matplotlib.pyplot as plt


# Distinct colors assigned to node labels so different entity types are visible.
_PALETTE = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
    "#59a14f", "#edc948", "#b07aa1", "#ff9da7",
]


def visualize(graph: nx.DiGraph, output_path: Optional[str] = None) -> None:
    """Draw the graph and either display it interactively or save to a file.

    Nodes are colored by their 'label' attribute; edge labels show the
    relationship type and optional weight.
    """
    if graph.number_of_nodes() == 0:
        print("Nothing to visualize — the graph is empty.")
        return

    # Assign a color to each unique node label.
    labels_seen: Dict[str, str] = {}
    node_colors: List[str] = []
    for _, data in graph.nodes(data=True):
        lbl = data.get("label", "unknown")
        if lbl not in labels_seen:
            labels_seen[lbl] = _PALETTE[len(labels_seen) % len(_PALETTE)]
        node_colors.append(labels_seen[lbl])

    pos = nx.spring_layout(graph, seed=42)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=700, alpha=0.9)
    nx.draw_networkx_labels(graph, pos, font_size=9)
    nx.draw_networkx_edges(graph, pos, arrows=True, arrowsize=20, edge_color="#888888")

    # Build edge labels from relationship name and optional weight.
    edge_labels: Dict[Tuple, str] = {}
    for src, tgt, data in graph.edges(data=True):
        parts = [data.get("label", "")]
        if "weight" in data:
            parts.append(f"w={data['weight']}")
        edge_labels[(src, tgt)] = " ".join(parts)

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=7)

    # Build a legend for node types.
    for label_name, color in labels_seen.items():
        plt.scatter([], [], c=color, s=100, label=label_name)
    plt.legend(scatterpoints=1, frameon=True, title="Node types")

    plt.title("Graph constructed from DSL")
    plt.axis("off")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150)
        print(f"Graph image saved to {output_path}")
    else:
        plt.show()

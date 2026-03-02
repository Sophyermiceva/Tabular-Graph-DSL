"""Graph builder — wraps networkx to construct a directed graph."""

from typing import Optional, Dict, Tuple

import networkx as nx

from dsl.errors import InterpreterError
from loader.csv_loader import Table


class GraphBuilder:
    """Incrementally builds a networkx DiGraph from interpreted DSL commands."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_nodes(self, label: str, key_field: str, table: Table) -> None:
        """Create a graph node for each unique key value in the table.

        Each node receives attributes: label (entity type) and the full row data.
        """
        if not table:
            return

        if key_field not in table[0]:
            raise InterpreterError(
                f"Key field '{key_field}' not found in table columns: "
                f"{list(table[0].keys())}"
            )

        for row in table:
            node_id = row[key_field]
            self.graph.add_node(node_id, label=label, **row)

    def add_edges(
        self,
        label: str,
        table: Table,
        source_field: str,
        target_field: str,
        weight_field: Optional[str] = None,
    ) -> None:
        """Create a directed edge for each row in the table.

        Optionally assigns a numeric weight from a specified column.
        """
        if not table:
            return

        columns = set(table[0].keys())
        for field_name, field_value in [("source", source_field), ("target", target_field)]:
            if field_value not in columns:
                raise InterpreterError(
                    f"Edge {field_name} field '{field_value}' not found in columns: "
                    f"{sorted(columns)}"
                )
        if weight_field and weight_field not in columns:
            raise InterpreterError(
                f"Weight field '{weight_field}' not found in columns: {sorted(columns)}"
            )

        for row in table:
            src = row[source_field]
            tgt = row[target_field]
            attrs: Dict = {"label": label}

            if weight_field:
                try:
                    attrs["weight"] = float(row[weight_field])
                except ValueError:
                    attrs["weight"] = row[weight_field]

            self.graph.add_edge(src, tgt, **attrs)

    def summary(self) -> str:
        """Return a human-readable summary of the graph."""
        lines = [
            f"Graph summary: {self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges",
            "",
            "Nodes:",
        ]
        for node, data in self.graph.nodes(data=True):
            lines.append(f"  [{data.get('label', '?')}] {node}")

        lines.append("")
        lines.append("Edges:")
        for src, tgt, data in self.graph.edges(data=True):
            weight_str = f" (weight={data['weight']})" if "weight" in data else ""
            lines.append(f"  {src} --[{data.get('label', '')}]--> {tgt}{weight_str}")

        return "\n".join(lines)

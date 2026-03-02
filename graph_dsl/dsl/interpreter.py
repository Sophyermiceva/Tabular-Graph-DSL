"""Interpreter — walks the AST and executes each statement.

The interpreter ties together the CSV loader and the graph builder.
It maintains a registry of loaded tables and delegates graph mutations
to the GraphBuilder.
"""

from pathlib import Path
from typing import Dict, List, Union

from dsl.ast_nodes import Statement, LoadStatement, NodeStatement, EdgeStatement
from dsl.errors import InterpreterError
from loader.csv_loader import load_csv, Table
from graph.builder import GraphBuilder


class Interpreter:
    """Executes a parsed DSL program (a list of AST statements)."""

    def __init__(self, data_dir: Union[str, Path] = "."):
        self.data_dir = Path(data_dir)
        self.tables: Dict[str, Table] = {}
        self.builder = GraphBuilder()

    def _resolve_table(self, name: str) -> Table:
        """Return a previously loaded table or raise an error."""
        if name not in self.tables:
            raise InterpreterError(
                f"Table '{name}' has not been loaded. "
                f"Add a LOAD {name}; statement before using it."
            )
        return self.tables[name]

    def _exec_load(self, stmt: LoadStatement) -> None:
        file_path = self.data_dir / f"{stmt.table_name}.csv"
        self.tables[stmt.table_name] = load_csv(file_path)
        print(f"  Loaded table '{stmt.table_name}' ({len(self.tables[stmt.table_name])} rows)")

    def _exec_node(self, stmt: NodeStatement) -> None:
        table = self._resolve_table(stmt.table_name)
        self.builder.add_nodes(stmt.label, stmt.key_field, table)
        print(f"  Created nodes [{stmt.label}] keyed by '{stmt.key_field}'")

    def _exec_edge(self, stmt: EdgeStatement) -> None:
        table = self._resolve_table(stmt.table_name)
        self.builder.add_edges(
            label=stmt.label,
            table=table,
            source_field=stmt.source_field,
            target_field=stmt.target_field,
            weight_field=stmt.weight_field,
        )
        weight_info = f" with weight '{stmt.weight_field}'" if stmt.weight_field else ""
        print(
            f"  Created edges [{stmt.label}] "
            f"{stmt.source_field} -> {stmt.target_field}{weight_info}"
        )

    def run(self, statements: List[Statement]) -> GraphBuilder:
        """Execute every statement and return the populated GraphBuilder."""
        print("Interpreter: executing DSL program...")
        for stmt in statements:
            if isinstance(stmt, LoadStatement):
                self._exec_load(stmt)
            elif isinstance(stmt, NodeStatement):
                self._exec_node(stmt)
            elif isinstance(stmt, EdgeStatement):
                self._exec_edge(stmt)
            else:
                raise InterpreterError(f"Unknown statement type: {type(stmt)}")
        print("Interpreter: done.\n")
        return self.builder

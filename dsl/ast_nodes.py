"""AST (Abstract Syntax Tree) node classes.

Each class represents a single statement type in the DSL.
The parser produces a list of these nodes; the interpreter consumes them.
"""

from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class LoadStatement:
    """LOAD <table_name>;"""
    table_name: str


@dataclass
class NodeStatement:
    """NODE <label> KEY <key_field> FROM <table_name>;"""
    label: str
    key_field: str
    table_name: str


@dataclass
class EdgeStatement:
    """
    EDGE <label>
        FROM <table_name>
        SOURCE <source_field>
        TARGET <target_field>
        [WEIGHT <weight_field>];
    """
    label: str
    table_name: str
    source_field: str
    target_field: str
    weight_field: Optional[str] = None


# Union type for any top-level statement.
Statement = Union[LoadStatement, NodeStatement, EdgeStatement]

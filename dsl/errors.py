"""Custom exception classes for DSL processing errors."""

from typing import Optional


class DSLError(Exception):
    """Base class for all DSL-related errors."""
    pass


class LexerError(DSLError):
    """Raised when the lexer encounters an unexpected character."""

    def __init__(self, char: str, line: int, col: int):
        self.char = char
        self.line = line
        self.col = col
        super().__init__(f"Unexpected character '{char}' at line {line}, column {col}")


class ParserError(DSLError):
    """Raised when the parser encounters an unexpected token."""

    def __init__(self, message: str, line: Optional[int] = None):
        self.line = line
        prefix = f"Line {line}: " if line else ""
        super().__init__(f"{prefix}{message}")


class InterpreterError(DSLError):
    """Raised during interpretation when data or references are invalid."""
    pass

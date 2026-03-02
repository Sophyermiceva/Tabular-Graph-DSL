"""Unit tests covering the full DSL pipeline: lexer → parser → interpreter."""

import unittest
from pathlib import Path

from dsl.lexer import Lexer
from dsl.parser import Parser
from dsl.interpreter import Interpreter
from dsl.ast_nodes import LoadStatement, NodeStatement, EdgeStatement
from dsl.errors import LexerError, ParserError, InterpreterError


EXAMPLES_DATA = Path(__file__).resolve().parent.parent / "examples" / "data"


class TestLexer(unittest.TestCase):

    def test_load_statement(self):
        tokens = Lexer("LOAD users;").tokenize()
        types = [t.type.name for t in tokens]
        self.assertEqual(types, ["LOAD", "IDENTIFIER", "SEMICOLON", "EOF"])

    def test_full_program(self):
        src = "LOAD t; NODE A KEY id FROM t;"
        tokens = Lexer(src).tokenize()
        self.assertTrue(len(tokens) > 0)
        self.assertEqual(tokens[-1].type.name, "EOF")

    def test_comment_skipping(self):
        src = "# this is a comment\nLOAD t;"
        tokens = Lexer(src).tokenize()
        types = [t.type.name for t in tokens]
        self.assertNotIn("COMMENT", types)
        self.assertIn("LOAD", types)

    def test_unexpected_character(self):
        with self.assertRaises(LexerError):
            Lexer("LOAD @invalid;").tokenize()


class TestParser(unittest.TestCase):

    def _parse(self, source: str):
        tokens = Lexer(source).tokenize()
        return Parser(tokens).parse()

    def test_load(self):
        stmts = self._parse("LOAD users;")
        self.assertEqual(len(stmts), 1)
        self.assertIsInstance(stmts[0], LoadStatement)
        self.assertEqual(stmts[0].table_name, "users")

    def test_node(self):
        stmts = self._parse("NODE User KEY id FROM users;")
        self.assertEqual(len(stmts), 1)
        self.assertIsInstance(stmts[0], NodeStatement)
        self.assertEqual(stmts[0].label, "User")
        self.assertEqual(stmts[0].key_field, "id")
        self.assertEqual(stmts[0].table_name, "users")

    def test_edge_with_weight(self):
        src = "EDGE Bought FROM orders SOURCE uid TARGET pid WEIGHT amt;"
        stmts = self._parse(src)
        self.assertEqual(len(stmts), 1)
        edge = stmts[0]
        self.assertIsInstance(edge, EdgeStatement)
        self.assertEqual(edge.weight_field, "amt")

    def test_edge_without_weight(self):
        src = "EDGE Follows FROM social SOURCE a TARGET b;"
        stmts = self._parse(src)
        edge = stmts[0]
        self.assertIsNone(edge.weight_field)

    def test_multiple_statements(self):
        src = """
        LOAD users;
        LOAD orders;
        NODE User KEY id FROM users;
        EDGE Bought FROM orders SOURCE user_id TARGET product_id WEIGHT amount;
        """
        stmts = self._parse(src)
        self.assertEqual(len(stmts), 4)

    def test_missing_semicolon(self):
        with self.assertRaises(ParserError):
            self._parse("LOAD users")

    def test_unexpected_token(self):
        with self.assertRaises(ParserError):
            self._parse("WEIGHT something;")


class TestInterpreter(unittest.TestCase):

    def test_full_pipeline(self):
        src = """
        LOAD users;
        LOAD orders;
        NODE User KEY id FROM users;
        NODE Product KEY product_id FROM orders;
        EDGE Bought FROM orders SOURCE user_id TARGET product_id WEIGHT amount;
        """
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        interpreter = Interpreter(data_dir=EXAMPLES_DATA)
        builder = interpreter.run(ast)

        g = builder.graph
        self.assertGreater(g.number_of_nodes(), 0)
        self.assertGreater(g.number_of_edges(), 0)

        # Users 1..4 + products P1, P2, P3 = 7 nodes
        self.assertEqual(g.number_of_nodes(), 7)
        # 6 order rows = 6 edges
        self.assertEqual(g.number_of_edges(), 6)

    def test_missing_table(self):
        src = "NODE User KEY id FROM nonexistent;"
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        interpreter = Interpreter(data_dir=EXAMPLES_DATA)
        with self.assertRaises(InterpreterError):
            interpreter.run(ast)

    def test_missing_column(self):
        src = """
        LOAD users;
        NODE User KEY nonexistent_column FROM users;
        """
        tokens = Lexer(src).tokenize()
        ast = Parser(tokens).parse()
        interpreter = Interpreter(data_dir=EXAMPLES_DATA)
        with self.assertRaises(InterpreterError):
            interpreter.run(ast)


if __name__ == "__main__":
    unittest.main()

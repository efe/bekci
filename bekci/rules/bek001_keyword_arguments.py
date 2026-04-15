from __future__ import annotations

import ast
from dataclasses import dataclass


ERROR_CODE = "BEK001"
ERROR_MESSAGE = f"{ERROR_CODE} use keyword arguments for calls with multiple arguments"


@dataclass(frozen=True, order=True)
class Violation:
    line: int
    column: int
    message: str


class KeywordArgumentVisitor(ast.NodeVisitor):
    """Find concrete positional arguments in calls that pass multiple arguments."""

    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_Call(self, node: ast.Call) -> None:
        if self._passes_multiple_arguments(node):
            positional_argument = self._first_concrete_positional_argument(node)
            if positional_argument is not None:
                self.violations.append(
                    Violation(
                        positional_argument.lineno,
                        positional_argument.col_offset,
                        ERROR_MESSAGE,
                    )
                )

        self.generic_visit(node)

    @staticmethod
    def _passes_multiple_arguments(node: ast.Call) -> bool:
        return len(node.args) + len(node.keywords) > 1

    @staticmethod
    def _first_concrete_positional_argument(node: ast.Call) -> ast.expr | None:
        for argument in node.args:
            if not isinstance(argument, ast.Starred):
                return argument

        return None

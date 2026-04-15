from __future__ import annotations

import ast
from collections.abc import Iterator
from typing import Any

from . import __version__
from .rules.bek001_keyword_arguments import KeywordArgumentVisitor, Violation


class Plugin:
    """Flake8 plugin adapter."""

    name = "bekci"
    version = __version__

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self) -> Iterator[tuple[int, int, str, type[Any]]]:
        for violation in self._violations():
            yield violation.line, violation.column, violation.message, type(self)

    def _violations(self) -> list[Violation]:
        visitor = KeywordArgumentVisitor()
        visitor.visit(self.tree)
        return sorted(visitor.violations)

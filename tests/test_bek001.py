from __future__ import annotations

import ast
import textwrap
import unittest

from bekci import Plugin


def run_plugin(source: str) -> list[tuple[int, int, str]]:
    tree = ast.parse(textwrap.dedent(source))
    return [(line, column, message) for line, column, message, _ in Plugin(tree).run()]


class Bek001KeywordArgumentRuleTest(unittest.TestCase):
    def test_allows_calls_with_no_arguments(self) -> None:
        self.assertEqual(run_plugin("func()"), [])

    def test_allows_calls_with_one_positional_argument(self) -> None:
        self.assertEqual(run_plugin("func(value)"), [])

    def test_allows_calls_with_one_keyword_argument(self) -> None:
        self.assertEqual(run_plugin("func(value=value)"), [])

    def test_allows_calls_with_multiple_keyword_arguments(self) -> None:
        self.assertEqual(run_plugin("func(first=1, second=2)"), [])

    def test_flags_multiple_positional_arguments(self) -> None:
        self.assertEqual(
            run_plugin("func(1, 2)"),
            [(1, 5, "BEK001 use keyword arguments for calls with multiple arguments")],
        )

    def test_flags_mixed_positional_and_keyword_arguments(self) -> None:
        self.assertEqual(
            run_plugin("func(1, second=2)"),
            [(1, 5, "BEK001 use keyword arguments for calls with multiple arguments")],
        )

    def test_counts_keyword_unpacking_when_deciding_if_call_has_multiple_arguments(
        self,
    ) -> None:
        self.assertEqual(
            run_plugin("func(value, **options)"),
            [(1, 5, "BEK001 use keyword arguments for calls with multiple arguments")],
        )

    def test_ignores_starred_positional_forwarding(self) -> None:
        self.assertEqual(run_plugin("func(*values, option=True)"), [])

    def test_visits_nested_calls(self) -> None:
        self.assertEqual(
            run_plugin("outer(inner(1, 2), value=3)"),
            [
                (1, 6, "BEK001 use keyword arguments for calls with multiple arguments"),
                (1, 12, "BEK001 use keyword arguments for calls with multiple arguments"),
            ],
        )


if __name__ == "__main__":
    unittest.main()

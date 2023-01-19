from __future__ import annotations

import pytest

from .core import gather_test_cases

__all__ = ("pytest_generate_tests", "pytest_configure")


def pytest_generate_tests(metafunc: pytest.Metafunc):
    func: pytest.Function = metafunc.definition
    suites = [m for m in func.own_markers if m.name == MARKER_NAME and m.kwargs]
    # If there is no marker, there's nothing to do.
    if not suites:
        return

    for marker in suites:
        # If the test is marked, but no matrix was provided, there's nothing to do.
        test_suite = marker.kwargs
        # Gather the test suite into a format pytest understands.
        ids, argnames, argvalues = gather_test_cases(test_suite=test_suite)
        metafunc.parametrize(
            argnames=argnames,
            argvalues=argvalues,
            ids=ids,
        )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers",
        f"{MARKER_NAME}: Easily define named test suites. "
        f"Ex: `@pytest.mark.{MARKER_NAME}(case1=dict(arg1=1, arg2=2), case2=...)`",
    )


MARKER_NAME = "suite"

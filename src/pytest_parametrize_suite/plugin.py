from __future__ import annotations

import pytest

from .core import gather_test_cases

__all__ = ("pytest_generate_tests", "pytest_configure")


def pytest_generate_tests(metafunc: pytest.Metafunc):
    func: pytest.Function = metafunc.definition
    matrix_marker = next((m for m in func.own_markers if m.name == MARKER_NAME), None)
    # If there is no marker, there's nothing to do.
    if matrix_marker is None:
        return

    # If the test is marked, but no matrix was provided, there's nothing to do.
    test_suite = matrix_marker.kwargs
    if not test_suite:
        return

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

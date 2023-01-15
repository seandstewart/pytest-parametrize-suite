from __future__ import annotations

import pytest

from pytest_parametrize_suite import core


def test_validate_suite_entry():
    # Given
    entry = dict(arg1=1)
    # When
    valid = core.validate_suite_entry(entry=entry)
    # Then
    assert valid


@pytest.mark.parametrize(
    argnames="entry", argvalues=["foo", {1: 1}], ids=["not-mapping", "non-str-keys"]
)
def test_validate_suite_entry_fails(entry):
    # When/Then
    with pytest.raises(ValueError):
        core.validate_suite_entry(entry=entry)


def test_gather_test_cases():
    # Given
    test_suite = dict(case1=dict(arg1=1))
    expected_test_cases = core.TestCases(
        ids=["case1"],
        argnames=["arg1"],
        argvalues=[(1,)],
    )
    # When
    test_cases = core.gather_test_cases(test_suite=test_suite)
    # Then
    assert test_cases == expected_test_cases


def test_gather_test_cases_invalid_shape():
    # Given
    test_suite = dict(
        case1=dict(arg1=1),
        # Extra argument
        case2=dict(arg1=1, arg2=2),
    )
    # When/Then
    with pytest.raises(ValueError):
        core.gather_test_cases(test_suite=test_suite)

from __future__ import annotations

import sys
from typing import Any, Mapping, NamedTuple

if sys.version_info < (3, 10):  # pragma: nocover
    from typing_extensions import TypeGuard
else:
    from typing import TypeGuard


def gather_test_cases(test_suite: Mapping[str, Any]) -> TestCases:
    """Collect test cases which we will pass onto `pytest.mark.parametrize`."""

    # Get the test ids for this matrix.
    ids = [*test_suite.keys()]
    # Grab the first entry in the matrix for initial validation.
    entry = next(iter(test_suite.values()))
    # Ensure the entry is of the appropriate type.
    validate_suite_entry(entry)
    # Determine the argnames we'll use for this matrix.
    entry_keys = entry.keys()
    argnames = [*entry_keys]
    argvalues: list[tuple] = []
    invalid: dict[int, Mapping[str, Any]] = {}

    for i, entry in enumerate(test_suite.values()):
        # If the entry isn't a mapping of the correct type, exit.
        validate_suite_entry(entry)
        # Otherwise, if the entry has a different shape, track the violation.
        if entry.keys() != entry_keys:
            invalid[i] = entry
            continue
        # Finally, if the entry is the correct type and shape, collect the argvalues.
        argvalues.append((*entry.values(),))

    # If there are entries of an incorrect shape, notify the user.
    if invalid:
        raise ValueError(
            f"Inconsistent shape for test matrix detected at index(es): {(*invalid,)}. "
            f"All matrix entries should have the same argnames. "
            f"(Detected: {argnames=})."
        )

    # Otherwise, return the collected test cases.
    return TestCases(ids=ids, argnames=argnames, argvalues=argvalues)


def validate_suite_entry(entry: Any) -> TypeGuard[Mapping[str, Any]]:
    """Validate that the given entry is of the correct type."""

    # The entry in the matrix must be a mapping and all keys must be string.
    if isinstance(entry, Mapping) and all(isinstance(k, str) for k in entry):
        return True
    raise ValueError(
        "Must define matrix entries as a mapping of argname->argvalue. "
        f"Got: {entry=}"
    )


class TestCases(NamedTuple):
    ids: list[str]
    argnames: list[str]
    argvalues: list[tuple]

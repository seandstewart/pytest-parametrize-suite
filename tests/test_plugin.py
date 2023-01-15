import pytest


@pytest.mark.suite(
    case1=dict(arg1=1, arg2=2),
    case2=dict(arg1=1, arg2=2),
)
def test_valid_suite(arg1, arg2):
    # Given
    expected_result = arg1
    # When
    result = arg2 - arg1
    # Then
    assert result == expected_result


def test_no_marker():
    assert True


@pytest.mark.suite()
def test_empty_suite():
    assert True

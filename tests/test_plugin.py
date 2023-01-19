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


@pytest.mark.suite(
    case1=dict(arg1="cross1"),
    case2=dict(arg1="cross2"),
)
@pytest.mark.suite(
    case3=dict(arg2="product1"),
    case4=dict(arg2="product2"),
)
def test_suite_matrix(arg1, arg2):
    # Given
    combination = arg1 + arg2
    # When
    possible_combinations.remove(combination)
    # Then
    assert combination not in possible_combinations


possible_combinations = {
    "cross1product1",
    "cross1product2",
    "cross2product1",
    "cross2product2",
}


def test_no_marker():
    assert True


@pytest.mark.suite()
def test_empty_suite():
    assert True

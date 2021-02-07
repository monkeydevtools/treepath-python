import pytest

from tests.utils.traverser_utils import assert_done_iterating, gen_test_data, naia, yaia, nyiy, yyia
from treepath import get, exp, find, match_all, match, wildcard, MatchNotFoundError


def test_empty_list_index_MatchNotFoundError():
    empty_list = []
    with pytest.raises(MatchNotFoundError):
        get(exp[0], empty_list)


def test_empty_list_wildcard_MatchNotFoundError():
    empty_list = []
    with pytest.raises(MatchNotFoundError):
        get(exp[wildcard], empty_list)


def test_3d_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(exp[10], three_dimensional_list)


def test_3d_0_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(exp[0][10], three_dimensional_list)


def test_3d_0_0_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(exp[0][0][10], three_dimensional_list)


def test_3d_0_10_0_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(exp[0][10][0], three_dimensional_list)


def test_list_on_key_MatchNotFoundError(k_a_a_k_a_a_a_k):
    with pytest.raises(MatchNotFoundError):
        get(exp[0], k_a_a_k_a_a_a_k)


def test_list_wildcard_on_key_MatchNotFoundError(k_a_a_k_a_a_a_k):
    with pytest.raises(MatchNotFoundError):
        get(exp[wildcard], k_a_a_k_a_a_a_k)


def test_3d_root(three_dimensional_list):
    expected = three_dimensional_list
    actual = get(exp, three_dimensional_list)
    assert actual == expected

def test_3d_0(three_dimensional_list):
    expected = three_dimensional_list[0]
    actual = get(exp[0], three_dimensional_list)
    assert actual == expected


def test_3d_0_path(three_dimensional_list):
    expected = three_dimensional_list[0]
    actual = match(exp[0], three_dimensional_list)
    assert str(actual) == f"$[0]={expected}"


def test_3d_0_0(three_dimensional_list):
    expected = three_dimensional_list[0][0]
    actual = get(exp[0][0], three_dimensional_list)
    assert actual == expected


def test_3d_0_0_path(three_dimensional_list):
    expected = three_dimensional_list[0][0]
    actual = match(exp[0][0], three_dimensional_list)
    assert str(actual) == f"$[0][0]={expected}"


def test_3d_0_0_0(three_dimensional_list):
    expected = three_dimensional_list[0][0][0]
    actual = get(exp[0][0][0], three_dimensional_list)
    assert actual == expected


def test_3d_0_0_0_path(three_dimensional_list):
    expected = three_dimensional_list[0][0][0]
    actual = match(exp[0][0][0], three_dimensional_list)
    assert str(actual) == f"$[0][0][0]={expected}"


def test_3d_find_all_slice(three_dimensional_list):
    result = find(exp[:][:][:], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_slice_path(three_dimensional_list):
    match_iter = match_all(exp[:][:][:], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, naia, naia, yaia):
        actual = next(match_iter)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(match_iter)


def test_a_k_k_a_k_k_k_a_find_all_slice(a_k_k_a_k_k_k_a):
    result = find(exp[:].y.y[:].y.y.y[:], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_slice_path(a_k_k_a_k_k_k_a):
    result = match_all(exp[:].y.y[:].y.y.y[:], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_slice(k_a_a_k_a_a_a_k):
    result = find(exp.y[:][:].y[:][:][:].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_slice_path(k_a_a_k_a_a_a_k):
    result = match_all(exp.y[:][:].y[:][:][:].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_3d_find_all_wildcard(three_dimensional_list):
    result = find(exp[wildcard][wildcard][wildcard], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_wildcard_path(three_dimensional_list):
    result = match_all(exp[wildcard][wildcard][wildcard], three_dimensional_list)
    for l1 in range(0, 3):
        for l2 in range(0, 3):
            for l3 in range(0, 3):
                actual = next(result)
                assert str(actual) == f"$[{l1}][{l2}][{l3}]={actual.data}"
    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard(a_k_k_a_k_k_k_a):
    result = find(exp[wildcard].y.y[wildcard].y.y.y[wildcard], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard_path(a_k_k_a_k_k_k_a):
    result = match_all(exp[wildcard].y.y[wildcard].y.y.y[wildcard], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard(k_a_a_k_a_a_a_k):
    result = find(exp.y[wildcard][wildcard].y[wildcard][wildcard][wildcard].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard_path(k_a_a_k_a_a_a_k):
    result = match_all(exp.y[wildcard][wildcard].y[wildcard][wildcard][wildcard].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_3d_find_specific_tuple(three_dimensional_list):
    result = find(exp[2, 3, "a", 1], three_dimensional_list)
    actual = next(result)
    expected = three_dimensional_list[2]
    assert actual == expected

    actual = next(result)
    expected = three_dimensional_list[1]
    assert actual == expected

    assert_done_iterating(result)


def test_3d_find_all_tuple(three_dimensional_list):
    result = find(exp[0, 1, 2][0, 1, 2][0, 1, 2], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_tuple_path(three_dimensional_list):
    match_iter = match_all(exp[0, 1, 2][0, 1, 2][0, 1, 2], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, naia, naia, yaia):
        actual = next(match_iter)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(match_iter)


def test_a_k_k_a_k_k_k_a_find_all_tuple(a_k_k_a_k_k_k_a):
    result = find(exp[0, 1, 2].y.y[0, 1, 2].y.y.y[0, 1, 2], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_tuple_path(a_k_k_a_k_k_k_a):
    result = match_all(exp[0, 1, 2].y.y[0, 1, 2].y.y.y[0, 1, 2], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple(k_a_a_k_a_a_a_k):
    result = find(exp.y[0, 1, 2][0, 1, 2].y[0, 1, 2][0, 1, 2][0, 1, 2].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple_path(k_a_a_k_a_a_a_k):
    result = match_all(exp.y[0, 1, 2][0, 1, 2].y[0, 1, 2][0, 1, 2][0, 1, 2].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)

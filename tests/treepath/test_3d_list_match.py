import pytest

from tests.utils.traverser_utils import assert_done_iterating, gen_test_data, naia, yaia, nyiy, yyia
from treepath import get, path, find, find_matches, get_match, wildcard, PopError
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_empty_list_index_MatchNotFoundError():
    empty_list = []
    with pytest.raises(MatchNotFoundError):
        get(path[0], empty_list)


def test_empty_list_wildcard_MatchNotFoundError():
    empty_list = []
    with pytest.raises(MatchNotFoundError):
        get(path[wildcard], empty_list)


def test_3d_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[10], three_dimensional_list)


def test_3d_0_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[0][10], three_dimensional_list)


def test_3d_0_0_10_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[0][0][10], three_dimensional_list)


def test_3d_0_10_0_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[0][10][0], three_dimensional_list)


def test_list_on_key_MatchNotFoundError(k_a_a_k_a_a_a_k):
    with pytest.raises(MatchNotFoundError):
        get(path[0], k_a_a_k_a_a_a_k)


def test_list_wildcard_on_key_MatchNotFoundError(k_a_a_k_a_a_a_k):
    with pytest.raises(MatchNotFoundError):
        get(path[wildcard], k_a_a_k_a_a_a_k)


def test_3d_root(three_dimensional_list):
    expected = three_dimensional_list
    actual = get(path, three_dimensional_list)
    assert actual == expected


def test_3d_0(three_dimensional_list):
    expected = three_dimensional_list[0]
    actual = get(path[0], three_dimensional_list)
    assert actual == expected


def test_3d_0_path(three_dimensional_list):
    expected = three_dimensional_list[0]
    actual = get_match(path[0], three_dimensional_list)
    assert str(actual) == f"$[0]={expected}"


def test_3d_0_0(three_dimensional_list):
    expected = three_dimensional_list[0][0]
    actual = get(path[0][0], three_dimensional_list)
    assert actual == expected


def test_3d_0_0_path(three_dimensional_list):
    expected = three_dimensional_list[0][0]
    actual = get_match(path[0][0], three_dimensional_list)
    assert str(actual) == f"$[0][0]={expected}"


def test_3d_0_0_0(three_dimensional_list):
    expected = three_dimensional_list[0][0][0]
    actual = get(path[0][0][0], three_dimensional_list)
    assert actual == expected


def test_3d_0_0_0_path(three_dimensional_list):
    expected = three_dimensional_list[0][0][0]
    actual = get_match(path[0][0][0], three_dimensional_list)
    assert str(actual) == f"$[0][0][0]={expected}"


def test_3d_find_all_slice(three_dimensional_list):
    result = find(path[:][:][:], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_slice_path(three_dimensional_list):
    match_iter = find_matches(path[:][:][:], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, naia, naia, yaia):
        actual = next(match_iter)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(match_iter)


def test_3d_find_all_slice_variety(three_dimensional_list):
    result = find(path[::-1][:1:][0::2], three_dimensional_list)
    for x in range(*slice(None, None, -1).indices(3)):
        for y in range(*slice(None, 1, None).indices(3)):
            for z in range(*slice(0, None, 2).indices(3)):
                actual = next(result)
                assert actual == three_dimensional_list[x][y][z]
    assert_done_iterating(result)


def test_3d_find_all_slice_variety_path(three_dimensional_list):
    test_data = [(expected_path, expected_value) for expected_path, expected_value in
                 gen_test_data(three_dimensional_list, naia, naia, yaia)]
    for actual in find_matches(path[::-1][:1:][0::2], three_dimensional_list):
        expected_path, expected_value = test_data[actual.data - 1]
        assert str(actual) == f"{expected_path}={expected_value}"


def test_3d_find_all_comma_delimited(three_dimensional_list):
    result = find(path[2, 1, 0][0, 1][0, 2, 1], three_dimensional_list)
    for x in [2, 1, 0]:
        for y in [0, 1]:
            for z in [0, 2, 1]:
                actual = next(result)
                assert actual == three_dimensional_list[x][y][z]
    assert_done_iterating(result)


def test_3d_find_all__comma_delimited_path(three_dimensional_list):
    test_data = [(expected_path, expected_value) for expected_path, expected_value in
                 gen_test_data(three_dimensional_list, naia, naia, yaia)]
    for actual in find_matches(path[2, 1, 0][0, 1][0, 2, 1], three_dimensional_list):
        expected_path, expected_value = test_data[actual.data - 1]
        assert str(actual) == f"{expected_path}={expected_value}"


def test_a_k_k_a_k_k_k_a_find_all_slice(a_k_k_a_k_k_k_a):
    result = find(path[:].y.y[:].y.y.y[:], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_slice_path(a_k_k_a_k_k_k_a):
    result = find_matches(path[:].y.y[:].y.y.y[:], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_slice(k_a_a_k_a_a_a_k):
    result = find(path.y[:][:].y[:][:][:].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_slice_path(k_a_a_k_a_a_a_k):
    result = find_matches(path.y[:][:].y[:][:][:].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_3d_find_all_wildcard(three_dimensional_list):
    result = find(path[wildcard][wildcard][wildcard], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_wildcard_path(three_dimensional_list):
    result = find_matches(path[wildcard][wildcard][wildcard], three_dimensional_list)
    for l1 in range(0, 3):
        for l2 in range(0, 3):
            for l3 in range(0, 3):
                actual = next(result)
                assert str(actual) == f"$[{l1}][{l2}][{l3}]={actual.data}"
    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard(a_k_k_a_k_k_k_a):
    result = find(path[wildcard].y.y[wildcard].y.y.y[wildcard], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard_path(a_k_k_a_k_k_k_a):
    result = find_matches(path[wildcard].y.y[wildcard].y.y.y[wildcard], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard(k_a_a_k_a_a_a_k):
    result = find(path.y[wildcard][wildcard].y[wildcard][wildcard][wildcard].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard_path(k_a_a_k_a_a_a_k):
    result = find_matches(path.y[wildcard][wildcard].y[wildcard][wildcard][wildcard].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_3d_find_specific_tuple(three_dimensional_list):
    result = find(path[2, 3, "a", 1], three_dimensional_list)
    actual = next(result)
    expected = three_dimensional_list[2]
    assert actual == expected

    actual = next(result)
    expected = three_dimensional_list[1]
    assert actual == expected

    assert_done_iterating(result)


def test_3d_find_all_tuple(three_dimensional_list):
    result = find(path[0, 1, 2][0, 1, 2][0, 1, 2], three_dimensional_list)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == expected
    assert_done_iterating(result)


def test_3d_find_all_tuple_path(three_dimensional_list):
    match_iter = find_matches(path[0, 1, 2][0, 1, 2][0, 1, 2], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, naia, naia, yaia):
        actual = next(match_iter)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(match_iter)


def test_a_k_k_a_k_k_k_a_find_all_tuple(a_k_k_a_k_k_k_a):
    result = find(path[0, 1, 2].y.y[0, 1, 2].y.y.y[0, 1, 2], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_tuple_path(a_k_k_a_k_k_k_a):
    result = find_matches(path[0, 1, 2].y.y[0, 1, 2].y.y.y[0, 1, 2], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, nyiy, nyiy, naia, nyiy, nyiy, nyiy, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple(k_a_a_k_a_a_a_k):
    result = find(path.y[0, 1, 2][0, 1, 2].y[0, 1, 2][0, 1, 2][0, 1, 2].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert actual == expected_value

    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple_path(k_a_a_k_a_a_a_k):
    result = find_matches(path.y[0, 1, 2][0, 1, 2].y[0, 1, 2][0, 1, 2][0, 1, 2].y, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, nyiy, naia, naia, nyiy, naia, naia, naia, yyia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_match_assign_set_0_0_0_to_2():
    actual = [[[1]]]
    expected = [[[2]]]
    match = get_match(path[0][0][0], actual)
    assert match.data == 1
    match.data = 2
    assert match.data == 2
    assert actual == expected


def test_match_del_0_0_0():
    actual = [[[1]]]
    expected = [[[]]]
    match = get_match(path[0][0][0], actual)
    assert match.data == 1
    del match.data
    assert actual == expected


def test_match_pop_0_0_0():
    actual = [[[1]]]
    expected = [[[]]]
    match = get_match(path[0][0][0], actual)
    assert match.data == 1
    actual_return = match.pop()
    assert actual_return == 1
    assert actual == expected


def test_match_pop_0_0_0_default():
    actual = [[[1]]]
    expected = [[[]]]
    match = get_match(path[0][0][0], actual)
    assert match.data == 1
    actual_return = match.pop(2)
    assert actual_return == 1
    actual_return = match.pop(2)
    assert actual_return == 2
    assert actual == expected


def test_match_pop_0_0_0_lookup_error():
    actual = [[[1]]]
    match = get_match(path[0][0][0], actual)
    assert match.data == 1
    actual_return = match.pop()
    assert actual_return == 1
    with pytest.raises(PopError) as exc_info:
        match.pop()
    actual = repr(exc_info.value)
    assert actual == "PopError(The reference data[0] does not exist.  Unable to del\n  path: $[0][0][0])"


def test_match_assign_set_0_0_to_0_2():
    actual = [[[2, 2]]]
    expected = [[[0]]]
    match = get_match(path[0][0], actual)
    assert match.data == [2, 2]
    match.data = [0]
    assert match.data == [0]
    assert actual == expected
    new_match = get_match(path[0], match)
    assert repr(new_match) == '$[0][0][0]=0'

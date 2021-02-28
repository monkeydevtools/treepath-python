from tests.utils.traverser_utils import *
from treepath import get, path, get_match, find, find_matches
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_empty_dict_index_MatchNotFoundError():
    empty_dict = {}
    with pytest.raises(MatchNotFoundError):
        get(path[0], empty_dict)


def test_empty_dict_wildcard_MatchNotFoundError():
    empty_dict = {}
    with pytest.raises(MatchNotFoundError):
        get(path.wildcard, empty_dict)


def test_keys_x_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path.a, keys)


def test_keys_x_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path.x.a, keys)


def test_keys_x_x_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path.x.x.a, keys)


def test_keys_x_a_x_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path.x.xx, keys)


def test_keys_x_on_list_MatchNotFoundError(a_k_k_a_k_k_k_a):
    with pytest.raises(MatchNotFoundError):
        get(path.x, a_k_k_a_k_k_k_a)


def test_keys_wildcard_on_list_MatchNotFoundError(a_k_k_a_k_k_k_a):
    with pytest.raises(MatchNotFoundError):
        get(path.wildcard, a_k_k_a_k_k_k_a)


def test_root_get(keys):
    expected = keys
    actual = get(path, keys)
    assert actual == expected


def test_keys_x(keys):
    expected = keys["x"]
    actual = get(path.x, keys)
    assert actual == expected


def test_keys_x_path(keys):
    expected = keys["x"]
    actual = get_match(path.x, keys)
    assert str(actual) == f"$.x={expected}"


def test_keys_x_find(keys):
    expected = keys["x"]
    for actual in find(path.x, keys):
        assert actual == expected


def test_keys_x_y(keys):
    expected = keys["x"]["y"]
    actual = get(path.x.y, keys)
    assert actual == expected


def test_keys_x_y_path(keys):
    expected = keys["x"]["y"]
    actual = get_match(path.x.y, keys)
    assert str(actual) == f"$.x.y={expected}"


def test_keys_x_y_z(keys):
    expected = keys["x"]["y"]["z"]
    actual = get(path.x.y.z, keys)
    assert actual == expected


def test_keys_x_y_z_path(keys):
    expected = keys["x"]["y"]["z"]
    actual = get_match(path.x.y.z, keys)
    assert str(actual) == f"$.x.y.z={expected}"


def test_keys_find_all_wildcard(keys):
    result = find(path.wildcard.wildcard.wildcard, keys)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == str(expected)
    assert_done_iterating(result)


def test_keys_find_all_wildcard_path(keys):
    result = find_matches(path.wildcard.wildcard.wildcard, keys)
    for expected_path, expected_value in gen_test_data(keys, naia, naia, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard(a_k_k_a_k_k_k_a):
    result = find(path[0].wc.wc[0].wc.wc.wc[0], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, n0i0, naia, naia, n0i0, naia, naia, naia, y0i0):
        actual = next(result)
        assert actual == expected_value
    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_wildcard_path(a_k_k_a_k_k_k_a):
    result = find_matches(path[0].wc.wc[0].wc.wc.wc[0], a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, n0i0, naia, naia, n0i0, naia, naia, naia, y0i0):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard(k_a_a_k_a_a_a_k):
    result = find(path.wc[0][0].wc[0][0][0].wc, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, n0i0, n0i0, naia, n0i0, n0i0, n0i0, yaia):
        actual = next(result)
        assert actual == expected_value
    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_wildcard_path(k_a_a_k_a_a_a_k):
    result = find_matches(path.wc[0][0].wc[0][0][0].wc, k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, n0i0, n0i0, naia, n0i0, n0i0, n0i0, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_keys_find_specific_tuple(keys):
    result = find(path["z", "a", 1, "x"], keys)

    actual = next(result)
    expected = keys["z"]
    assert actual == expected

    actual = next(result)
    expected = keys["x"]
    assert actual == expected

    assert_done_iterating(result)


def test_keys_find_all_tuple(keys):
    result = find(path["x", "y", "z"]["x", "y", "z"]["x", "y", "z"], keys)
    for expected in range(1, 28):
        actual = next(result)
        assert actual == str(expected)
    assert_done_iterating(result)


def test_keys_find_all_tuple_path(keys):
    match_iter = find_matches(path["x", "y", "z"]["x", "y", "z"]["x", "y", "z"], keys)
    for expected_path, expected_value in gen_test_data(keys, naia, naia, yaia):
        actual = next(match_iter)
        assert str(actual) == f"{expected_path}={actual.data}"


def test_a_k_k_a_k_k_k_a_find_all_tuple(a_k_k_a_k_k_k_a):
    result = find(path[0]["x", "y", "z"]["x", "y", "z"][0]["x", "y", "z"]["x", "y", "z"]["x", "y", "z"][0],
                  a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, n0i0, naia, naia, n0i0, naia, naia, naia, y0i0):
        actual = next(result)
        assert actual == expected_value
    assert_done_iterating(result)


def test_a_k_k_a_k_k_k_a_find_all_tuple_path(a_k_k_a_k_k_k_a):
    result = find_matches(path[0]["x", "y", "z"]["x", "y", "z"][0]["x", "y", "z"]["x", "y", "z"]["x", "y", "z"][0],
                          a_k_k_a_k_k_k_a)
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, n0i0, naia, naia, n0i0, naia, naia, naia, y0i0):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple(k_a_a_k_a_a_a_k):
    result = find(path["x", "y", "z"][0][0]["x", "y", "z"][0][0][0]["x", "y", "z"], k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, n0i0, n0i0, naia, n0i0, n0i0, n0i0, yaia):
        actual = next(result)
        assert actual == expected_value
    assert_done_iterating(result)


def test_k_a_a_k_a_a_a_k_find_all_tuple_path(k_a_a_k_a_a_a_k):
    result = find_matches(path["x", "y", "z"][0][0]["x", "y", "z"][0][0][0]["x", "y", "z"], k_a_a_k_a_a_a_k)
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, n0i0, n0i0, naia, n0i0, n0i0, n0i0, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={expected_value}"
    assert_done_iterating(result)

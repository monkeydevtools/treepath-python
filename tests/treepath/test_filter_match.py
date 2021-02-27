from tests.utils.traverser_utils import *
from treepath import get, path, match_all, has, match, wc, find
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_keys_get_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path.a)], keys)


def test_keys_get_root_has_x(keys):
    expected = keys
    actual = get(path[has(path.x)], keys)
    assert actual == expected


def test_keys_get_root_x_were_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path.a)].x, keys)


def test_keys_get_root_x_were_root_has_y(keys):
    expected = keys["x"]
    actual = get(path[has(path.y)].x, keys)
    assert actual == expected


def test_keys_match_all_root_wc_has_x(keys):
    result = match_all(path.wc[has(path.x)], keys)
    for expected_path, expected_value in gen_test_data(keys, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_keys_match_all_root_wc_has_a(keys):
    result = match_all(path.wc[has(path.a)], keys)
    assert_done_iterating(result)


def test_keys_match_all_all_has_x(keys):
    exp_iter = match_all(path.rec[has(path.x)], keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_keys_match_all_all_has_a(keys):
    exp_iter = match_all(path.rec[has(path.a)], keys)
    assert_done_iterating(exp_iter)


def test_keys_match_all_all_has_x_eq_1(keys):
    exp_iter = match_all(path.rec.x[has(path.rec.x == "1")], keys)
    actual = next(exp_iter)
    expected = match(path.x, keys)
    assert repr(actual) == repr(expected)

    actual = next(exp_iter)
    expected = match(path.x.x, keys)
    assert repr(actual) == repr(expected)

    assert_done_iterating(exp_iter)


def test_keys_lt(keys):
    expected = [str(v) for v in range(1, 14)]
    actual = [v for v in find(path.wc.wc.wc[has(path < 14, int)], keys)]
    assert actual == expected


def test_keys_le(keys):
    expected = [str(v) for v in range(1, 15)]
    actual = [v for v in find(path.wc.wc.wc[has(path <= 14, int)], keys)]
    assert actual == expected


def test_keys_eq(keys):
    expected = ["14"]
    actual = [v for v in find(path.wc.wc.wc[has(path == 14, int)], keys)]
    assert actual == expected


def test_keys_ne(keys):
    expected = [str(v) for v in range(1, 28)]
    expected.remove("14")
    actual = [v for v in find(path.wc.wc.wc[has(path != 14, int)], keys)]
    assert actual == expected


def test_keys_gt(keys):
    expected = [str(v) for v in range(15, 28)]
    actual = [v for v in find(path.wc.wc.wc[has(path > 14, int)], keys)]
    assert actual == expected


def test_keys_ge(keys):
    expected = [str(v) for v in range(14, 28)]
    actual = [v for v in find(path.wc.wc.wc[has(path >= 14, int)], keys)]
    assert actual == expected


def test_3d_list_get_root_has_a_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path[4])], three_dimensional_list)


def test_3d_list_get_root_has_1(three_dimensional_list):
    expected = three_dimensional_list
    actual = get(path[has(path[1])], three_dimensional_list)
    assert actual == expected


def test_3d_list_get_root_1_were_root_has_a_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path[4])][1], three_dimensional_list)


def test_3d_list_get_root_1_were_root_has_1(three_dimensional_list):
    expected = three_dimensional_list[1]
    actual = get(path[has(path[1])][1], three_dimensional_list)
    assert actual == expected


def test_3d_list_match_all_root_wc_has_1(three_dimensional_list):
    result = match_all(path[wc][has(path[1])], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_3d_list_match_all_root_wc_has_a(three_dimensional_list):
    result = match_all(path[wc][has(path[4])], three_dimensional_list)
    assert_done_iterating(result)


def test_3d_list_match_all_all_has_1(three_dimensional_list):
    exp_iter = match_all(path.rec[has(path[1])], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_3d_list_match_all_all_has_a(three_dimensional_list):
    exp_iter = match_all(path.rec[has(path[4])], three_dimensional_list)
    assert_done_iterating(exp_iter)


def test_3d_list_match_all_all_has_1_eq_1(three_dimensional_list):
    exp_iter = match_all(path.rec[1][has(path.rec[1] == 14)], three_dimensional_list)
    actual = next(exp_iter)
    expected = match(path[1], three_dimensional_list)
    assert repr(actual) == repr(expected)

    actual = next(exp_iter)
    expected = match(path[1][1], three_dimensional_list)
    assert repr(actual) == repr(expected)

    assert_done_iterating(exp_iter)


def test_3d_list_lt(three_dimensional_list):
    expected = [v for v in range(1, 14)]
    actual = [v for v in find(path[wc][wc][wc][has(path < 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_le(three_dimensional_list):
    expected = [v for v in range(1, 15)]
    actual = [v for v in find(path[wc][wc][wc][has(path <= 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_eq(three_dimensional_list):
    expected = [14]
    actual = [v for v in find(path[wc][wc][wc][has(path == 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_ne(three_dimensional_list):
    expected = [v for v in range(1, 28)]
    expected.remove(14)
    actual = [v for v in find(path[wc][wc][wc][has(path != 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_gt(three_dimensional_list):
    expected = [v for v in range(15, 28)]
    actual = [v for v in find(path[wc][wc][wc][has(path > 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_ge(three_dimensional_list):
    expected = [v for v in range(14, 28)]
    actual = [v for v in find(path[wc][wc][wc][has(path >= 14)], three_dimensional_list)]
    assert actual == expected

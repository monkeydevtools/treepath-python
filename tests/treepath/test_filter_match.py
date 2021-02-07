import pytest

from tests.utils.traverser_utils import *
from treepath import get, exp, match_all, MatchNotFoundError, has


def test_keys_get_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(exp[has(exp.a)], keys)


def test_keys_get_root_has_x(keys):
    expected = keys
    actual = get(exp[has(exp.x)], keys)
    assert actual == expected


def test_keys_get_root_x_were_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(exp[has(exp.a)].x, keys)


def test_keys_get_root_x_were_root_has_x(keys):
    expected = keys["x"]
    actual = get(exp[has(exp.x)].x, keys)
    assert actual == expected


def test_keys_find_root_wc_has_x(keys):
    result = match_all(exp.wc[has(exp.x)], keys)
    for expected_path, expected_value in gen_test_data(keys, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_keys_find_root_wc_has_a(keys):
    result = match_all(exp.wc[has(exp.a)], keys)
    assert_done_iterating(result)


def test_keys_find_all_has_x(keys):
    exp_iter = match_all(exp.rec[has(exp.x)], keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_keys_find_all_has_a(keys):
    exp_iter = match_all(exp.rec[has(exp.a)], keys)
    assert_done_iterating(exp_iter)
    

def test_keys_find_all_has_x_eq_1(keys):
    exp_iter = match_all(exp.rec.x[has(exp.rec.x == "1")], keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)

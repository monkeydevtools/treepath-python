from tests.utils.traverser_utils import *
from treepath import find, exp, match_all


def test_recursive_find_all_keys(keys):
    exp_iter = find(exp.recursive, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 40
    assert_done_iterating(exp_iter)


def test_recursive_find_all_keys_path(keys):
    exp_iter = match_all(exp.recursive, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 40
    assert_done_iterating(exp_iter)


def test_recursive_find_all_three_dimensional_list(three_dimensional_list):
    exp_iter = find(exp.recursive, three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 40
    assert_done_iterating(exp_iter)


def test_recursive_find_all_three_dimensional_list_path(three_dimensional_list):
    exp_iter = match_all(exp.recursive, three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 40
    assert_done_iterating(exp_iter)


def test_recursive_find_all_k_a_a_k_a_a_a_k(k_a_a_k_a_a_a_k):
    exp_iter = find(exp.recursive, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 9841
    assert_done_iterating(exp_iter)


def test_recursive_find_all_k_a_a_k_a_a_a_k_path(k_a_a_k_a_a_a_k):
    exp_iter = match_all(exp.recursive, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 9841
    assert_done_iterating(exp_iter)


def test_recursive_find_all_a_k_k_a_k_k_k_a(a_k_k_a_k_k_k_a):
    exp_iter = find(exp.recursive, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 9841
    assert_done_iterating(exp_iter)


def test_recursive_find_all_a_k_k_a_k_k_k_a_path(a_k_k_a_k_k_k_a):
    exp_iter = match_all(exp.recursive, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 9841
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_keys(keys):
    exp_iter = find(exp.recursive.x, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 13
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_keys_path(keys):
    exp_iter = match_all(exp.recursive.x, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_three_dimensional_list(three_dimensional_list):
    exp_iter = find(exp.recursive[0], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, y0ia, y0ia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 13
    assert_done_iterating(exp_iter)


def test_recursive_find_all_o_three_dimensional_list_path(three_dimensional_list):
    exp_iter = match_all(exp.recursive[0], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, y0ia, y0ia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_k_a_a_k_a_a_a_k(k_a_a_k_a_a_a_k):
    exp_iter = find(exp.recursive.x, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yxia, naia, naia, yxia, naia, naia, naia, yxia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 2215
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_k_a_a_k_a_a_a_k_path(k_a_a_k_a_a_a_k):
    exp_iter = match_all(exp.recursive.x, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yxia, naia, naia, yxia, naia, naia, naia, yxia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 2215
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_a_k_k_a_k_k_k_a(a_k_k_a_k_k_k_a):
    exp_iter = find(exp.recursive.x, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, yxia, yxia, naia, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 1065
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_a_k_k_a_k_k_k_a_path(a_k_k_a_k_k_k_a):
    exp_iter = match_all(exp.recursive.x, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, yxia, yxia, naia, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 1065
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_k_a_a_k_a_a_a_k(k_a_a_k_a_a_a_k):
    exp_iter = find(exp.recursive[0], k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, y0ia, y0ia, naia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 1065
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_k_a_a_k_a_a_a_k_path(k_a_a_k_a_a_a_k):
    exp_iter = match_all(exp.recursive[0], k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, y0ia, y0ia, naia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 1065
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_a_k_k_a_k_k_k_a(a_k_k_a_k_k_k_a):
    exp_iter = find(exp.recursive[0], a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, y0ia, naia, naia, y0ia, naia, naia, naia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 2215
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_a_k_k_a_k_k_k_a_path(a_k_k_a_k_k_k_a):
    exp_iter = match_all(exp.recursive[0], a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, y0ia, naia, naia, y0ia, naia, naia, naia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 2215
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_all_data_types(all_data_types):
    exp_iter = find(exp.recursive.x, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, yxia, yxia, yxia, yxia, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 5
    assert_done_iterating(exp_iter)


def test_recursive_find_all_x_all_data_types_path(all_data_types):
    exp_iter = match_all(exp.recursive.x, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, yxia, yxia, yxia, yxia, yxia, yxia, yxia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 5
    assert_done_iterating(exp_iter)


def test_recursive_find_all_0_all_data_types(all_data_types):
    exp_iter = find(exp.recursive[0], all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, y0ia, y0ia, y0ia, y0ia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(exp_iter)
        assert actual == expected_value
    assert count == 7
    assert_done_iterating(exp_iter)


def test_recursive_find_all_nested_xs_under_each_y_keys(keys):
    exp_iter = find(exp.rec.y.rec.x, keys)
    expected_values = []
    for _, value in gen_test_data(keys, yyia, yyia, yyia):
        for _, expected_value in gen_test_data(value, yxia, yxia, yxia):
            expected_values.append(expected_value)
    assert len(expected_values) == 7
    for actual in exp_iter:
        expected_values.remove(actual)
    assert len(expected_values) == 0


def test_recursive_find_all_nested_0s_under_each_1_three_dimensional_list(three_dimensional_list):
    exp_iter = find(exp.rec[1].rec[0], three_dimensional_list)
    expected_values = []
    for _, value in gen_test_data(three_dimensional_list, y1ia, y1ia, y1ia):
        for _, expected_value in gen_test_data(value, y0ia, y0ia, y0ia):
            expected_values.append(expected_value)
    assert len(expected_values) == 7
    for actual in exp_iter:
        expected_values.remove(actual)
    assert len(expected_values) == 0

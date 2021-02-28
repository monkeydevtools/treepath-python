from tests.utils.traverser_utils import *
from treepath import find, path, find_matches


def test_keys_recursive_find_all(keys):
    find_iter = find(path.recursive, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 40
    assert_done_iterating(find_iter)


def test_keys_recursive_find_all_path(keys):
    find_iter = find_matches(path.recursive, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 40
    assert_done_iterating(find_iter)


def test_keys_recursive_find_all_path_start_with_x(keys):
    find_iter = find_matches(path.x.recursive, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxix, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(find_iter)


def test_3d_list_recursive_find_all(three_dimensional_list):
    find_iter = find(path.recursive, three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 40
    assert_done_iterating(find_iter)


def test_3d_list_recursive_find_all_path(three_dimensional_list):
    find_iter = find_matches(path.recursive, three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 40
    assert_done_iterating(find_iter)


def test_3d_list_recursive_find_all_path_start_with_0(three_dimensional_list):
    find_iter = find_matches(path[0].recursive, three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, y0i0, yaia, yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all(k_a_a_k_a_a_a_k):
    find_iter = find(path.recursive, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 9841
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all_path(k_a_a_k_a_a_a_k):
    find_iter = find_matches(path.recursive, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 9841
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all(a_k_k_a_k_k_k_a):
    find_iter = find(path.recursive, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 9841
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all_path(a_k_k_a_k_k_k_a):
    find_iter = find_matches(path.recursive, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, yria, yaia, yaia, yaia, yaia, yaia, yaia, yaia,
                                                       yaia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 9841
    assert_done_iterating(find_iter)


def test_keys_recursive_find_all_x(keys):
    find_iter = find(path.recursive.x, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 13
    assert_done_iterating(find_iter)


def test_keys_recursive_find_all_x_path(keys):
    find_iter = find_matches(path.recursive.x, keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(find_iter)


def test_3d_list_recursive_find_all_0(three_dimensional_list):
    find_iter = find(path.recursive[0], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, y0ia, y0ia, y0ia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 13
    assert_done_iterating(find_iter)


def test_3d_list_recursive_find_all_o_path(three_dimensional_list):
    find_iter = find_matches(path.recursive[0], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, y0ia, y0ia, y0ia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all_x(k_a_a_k_a_a_a_k):
    find_iter = find(path.recursive.x, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yxia, naia, naia, yxia, naia, naia, naia, yxia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2215
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all_x_path(k_a_a_k_a_a_a_k):
    find_iter = find_matches(path.recursive.x, k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, yxia, naia, naia, yxia, naia, naia, naia, yxia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 2215
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all_x(a_k_k_a_k_k_k_a):
    find_iter = find(path.recursive.x, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, yxia, yxia, naia, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 1065
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all_x_path(a_k_k_a_k_k_k_a):
    find_iter = find_matches(path.recursive.x, a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, naia, yxia, yxia, naia, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 1065
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all_0(k_a_a_k_a_a_a_k):
    find_iter = find(path.recursive[0], k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, y0ia, y0ia, naia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 1065
    assert_done_iterating(find_iter)


def test_k_a_a_k_a_a_a_k_recursive_find_all_0_path(k_a_a_k_a_a_a_k):
    find_iter = find_matches(path.recursive[0], k_a_a_k_a_a_a_k)
    count = 0
    for expected_path, expected_value in gen_test_data(k_a_a_k_a_a_a_k, naia, y0ia, y0ia, naia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 1065
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all_0(a_k_k_a_k_k_k_a):
    find_iter = find(path.recursive[0], a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, y0ia, naia, naia, y0ia, naia, naia, naia, y0ia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2215
    assert_done_iterating(find_iter)


def test_a_k_k_a_k_k_k_a_recursive_find_all_0_path(a_k_k_a_k_k_k_a):
    find_iter = find_matches(path.recursive[0], a_k_k_a_k_k_k_a)
    count = 0
    for expected_path, expected_value in gen_test_data(a_k_k_a_k_k_k_a, y0ia, naia, naia, y0ia, naia, naia, naia, y0ia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 2215
    assert_done_iterating(find_iter)


def test_all_data_types_recursive_find_all_x(all_data_types):
    find_iter = find(path.recursive.x, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, yxia, yxia, yxia, yxia, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 5
    assert_done_iterating(find_iter)


def test_all_data_types_recursive_find_all_x_path(all_data_types):
    find_iter = find_matches(path.recursive.x, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, yxia, yxia, yxia, yxia, yxia, yxia, yxia):
        count += 1
        actual = next(find_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 5
    assert_done_iterating(find_iter)


def test_all_data_types_recursive_find_all_0(all_data_types):
    find_iter = find(path.recursive[0], all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, y0ia, y0ia, y0ia, y0ia, y0ia, y0ia, y0ia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 7
    assert_done_iterating(find_iter)


def test_keys_recursive_find_all_nested_xs_under_each_y(keys):
    find_iter = find(path.rec.y.rec.x, keys)
    expected_values = []
    for _, value in gen_test_data(keys, yyia, yyia, yyia):
        for _, expected_value in gen_test_data(value, yxia, yxia, yxia):
            expected_values.append(expected_value)
    assert len(expected_values) == 7
    for actual in find_iter:
        expected_values.remove(actual)
    assert len(expected_values) == 0


def test_3d_list_recursive_find_all_nested_0s_under_each_1(three_dimensional_list):
    find_iter = find(path.rec[1].rec[0], three_dimensional_list)
    expected_values = []
    for _, value in gen_test_data(three_dimensional_list, y1ia, y1ia, y1ia):
        for _, expected_value in gen_test_data(value, y0ia, y0ia, y0ia):
            expected_values.append(expected_value)
    assert len(expected_values) == 7
    for actual in find_iter:
        expected_values.remove(actual)
    assert len(expected_values) == 0

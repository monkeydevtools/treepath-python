from tests.utils.traverser_utils import *
from treepath import find, path, wc, gwc


def test_key_generic_wildcard_level_1(all_data_types):
    find_iter = find(path.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_2(all_data_types):
    find_iter = find(path.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_3(all_data_types):
    find_iter = find(path.gwc.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 4
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_4(all_data_types):
    find_iter = find(path.gwc.gwc.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 4
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_5(all_data_types):
    find_iter = find(path.gwc.gwc.gwc.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_6(all_data_types):
    find_iter = find(path.gwc.gwc.gwc.gwc.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, naia, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 5
    assert_done_iterating(find_iter)


def test_key_generic_wildcard_level_7(all_data_types):
    find_iter = find(path.gwc.gwc.gwc.gwc.gwc.gwc.gwc, all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, naia, naia, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 2
    assert_done_iterating(find_iter)


def test_list_generic_wildcard_level_6(all_data_types):
    find_iter = find(path[gwc][gwc][gwc][gwc][gwc][gwc], all_data_types)
    count = 0
    for expected_path, expected_value in gen_test_data(all_data_types, naia, naia, naia, naia, naia, yaia):
        count += 1
        actual = next(find_iter)
        assert actual == expected_value
    assert count == 5
    assert_done_iterating(find_iter)



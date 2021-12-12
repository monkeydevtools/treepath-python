import pytest

from treepath import path, set_, SetError, wc, has, set_match


def test_set_a_to_1_invalid_type():
    expected = "SetError(Invalid assignment data[0] = 1 because data is of type: <class \'dict\'>, expecting " \
               "type: <class \'list\'>\n" \
               "  path: $[0])"""
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[0], 1, empty_dict)
    actual = repr(exc_info.value)
    assert actual == expected


def test_set_0_to_1_invalid_type():
    expected = "SetError(Invalid assignment data['a'] = 1 because data is of type: <class \'list\'>, expecting " \
               "type: <class \'dict\'>\n" \
               "  path: $.a)"""
    empty_list = []
    with pytest.raises(SetError) as exc_info:
        set_(path.a, 1, empty_list)
    assert repr(exc_info.value) == expected


def test_set_0_to_1_index_out_of_range():
    expected = "SetError(The path $[1] index is out of range.  " \
               "The index must be in the range 0 >= index <=0.  To append the index must the list current length." \
               "\n  path: $[1])"
    empty_list = []
    with pytest.raises(SetError) as exc_info:
        set_(path[1], 1, empty_list)
    assert repr(exc_info.value) == expected


def test_set_wc_to_1_invalid_path():
    expected = "SetError(The path $[*] does not support set.  It can only be a key or index\n  path: $[*])"
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[wc], 1, empty_dict)
    assert repr(exc_info.value) == expected


def test_set_wc_a_to_1_invalid_path_cascade():
    expected = "SetError(The path $[*] does not support set.  It can only be a key or index\n  path: $[*])"
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[wc].a, 1, empty_dict, cascade=True)
    assert repr(exc_info.value) == expected


def test_set_a_b_c_to_1_no_cascade_expect_error():
    actual = {"x": 2}
    expected = "SetError(The parent path $.a.b does not exist.  It must be created first or use cascade to auto " \
               "create it.\n" \
               "  path: $.a.b.c)"

    with pytest.raises(SetError) as exc_info:
        set_(path.a.b.c, 1, actual)
    pretty_error_msg = repr(exc_info.value)
    assert pretty_error_msg == expected


def test_set_a_to_1_empty_data():
    actual = dict()
    expected = {"a": 1}
    set_(path.a, 1, actual)
    assert actual == expected


def test_set_a_to_1():
    actual = {"a": 0, "x": 2}
    expected_return = 1
    expected = {"a": 1, "x": 2}
    actual_return = set_(path.a, 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_a_to_1_predicate():
    actual = {"a": 0, "x": 2}
    expected_return = 1
    expected = {"a": 1, "x": 2}
    actual_return = set_(path[has(path.a == 0)].a, 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_a_b_c_to_1_empty_data_cascade():
    actual = dict()
    expected_return = 1
    expected = {"a": {"b": {"c": 1}}}
    actual_return = set_(path.a.b.c, 1, actual, cascade=True)
    assert actual == expected
    assert actual_return == expected_return


def test_set_a_b_c_to_1__with_b_empty_data():
    actual = {"a": {"b": {}}}
    expected_return = 1
    expected = {"a": {"b": {"c": 1}}}
    actual_return = set_(path.a.b.c, 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_a_b_c_to_1_cascade():
    actual = {"x": 2}
    expected_return = 1
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    actual_return = set_(path.a.b.c, 1, actual, cascade=True)
    assert actual == expected
    assert actual_return == expected_return


def test_set_match_a_b_c_to_1_cascade():
    actual = {"x": 2}
    expected_return = '$.a.b.c=1'
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    actual_return = set_match(path.a.b.c, 1, actual, cascade=True)
    assert actual == expected
    assert repr(actual_return) == expected_return


def test_set_a_b_c_to_1_a_is_int_cascade_error():
    actual = {"a": 2}
    expected = "SetError(Invalid assignment data['b'] = {} because data is of type: <class 'int'>, expecting type: " \
               "<class 'dict'>\n" \
               "  path: $.a.b)"

    with pytest.raises(SetError) as exc_info:
        set_(path.a.b.c, 1, actual, cascade=True)
    pretty_error_msg = repr(exc_info.value)
    assert pretty_error_msg == expected


def test_set_0_to_1_empty_data_append():
    actual = list()
    expected_return = 1
    expected = [1]
    actual_return = set_(path[0], 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_0_to_1():
    actual = [0, 2]
    expected_return = 1
    expected = [1, 2]
    actual_return = set_(path[0], 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_0_to_1_append():
    actual = [0, 2]
    expected_return = 1
    expected = [0, 2, 1]
    actual_return = set_(path[2], 1, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_set_0_0_0_to_1_empty_data_cascade():
    actual = list()
    expected_return = 1
    expected = [[[1]]]
    actual_return = set_(path[0][0][0], 1, actual, cascade=True)
    assert actual == expected
    assert actual_return == expected_return


def test_set_0_0_0_to_1_and_0_is_int_cascade_error():
    actual = [0, 2]
    expected = "SetError(Invalid assignment data[0] = [] because data is of type: <class 'int'>, expecting type: " \
               "<class 'list'>\n" \
               "  path: $[0][0])"

    with pytest.raises(SetError) as exc_info:
        set_(path[0][0][0], 1, actual, cascade=True)
    pretty_error_msg = repr(exc_info.value)
    assert pretty_error_msg == expected


def test_set_2_0_0_to_1_cascade():
    actual = [0, 2]
    expected_return = 1
    expected = [0, 2, [[1]]]
    actual_return = set_(path[2][0][0], 1, actual, cascade=True)
    assert actual == expected
    assert actual_return == expected_return

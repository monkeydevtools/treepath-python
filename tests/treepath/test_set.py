import pytest

from treepath import path, set_, SetError, wc


def test_set_a_to_1_invalid_type():
    expected = "SetError(The vertex $ does not support set.  It can only be key or index)"
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[0], 1, empty_dict)
    assert repr(exc_info.value) == expected


def test_set_0_to_1_invalid_type():
    expected = "SetError(The data type <class 'list'> is invalid. The type must be <class 'dict'>\n  path: $.a)"
    empty_list = []
    with pytest.raises(SetError) as exc_info:
        set_(path.a, 1, empty_list)
    assert repr(exc_info.value) == expected


def test_set_1_to_1_index_out_of_range():
    expected = "SetError(The vertex $[1] index is out of range.  " \
               "The index must be in the range 0 >= index <=0\n  path: $[1])"
    empty_list = []
    with pytest.raises(SetError) as exc_info:
        set_(path[1], 1, empty_list)
    assert repr(exc_info.value) == expected


def test_set_wc_to_1_invalid_vertex():
    expected = "SetError(The vertex $[*] does not support set.  It can only be key or index\n  path: $[*])"
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[wc], 1, empty_dict)
    assert repr(exc_info.value) == expected


def test_set_wc_a_to_1_invalid_vertex():
    expected = "SetError(The vertex $[*] does not support set.  It can only be key or index\n  path: $[*])"
    empty_dict = {}
    with pytest.raises(SetError) as exc_info:
        set_(path[wc].a, 1, empty_dict)
    assert repr(exc_info.value) == expected


def test_set_a_to_1_empty_data():
    actual = dict()
    expected = {"a": 1}
    set_(path.a, 1, actual)
    assert actual == expected


def test_set_a_to_1_dirty_date():
    actual = {"a": 0, "x": 2}
    expected = {"a": 1, "x": 2}
    set_(path.a, 1, actual)
    assert actual == expected


def test_set_a_b_c_to_1_empty_data():
    actual = dict()
    expected = {"a": {"b": {"c": 1}}}
    set_(path.a.b.c, 1, actual)
    assert actual == expected


def test_set_a_b_c_to_1_dirty_data():
    actual = {"x": 2}
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    set_(path.a.b.c, 1, actual)
    assert actual == expected


def test_set_0_to_1_empty_data():
    actual = list()
    expected = [1]
    set_(path[0], 1, actual)
    assert actual == expected


def test_set_0_to_1_dirty_date():
    actual = [0, 2]
    expected = [1, 2]
    set_(path[0], 1, actual)
    assert actual == expected


def test_set_0_0_0_to_1_empty_data():
    actual = list()
    expected = [[[1]]]
    set_(path[0][0][0], 1, actual)
    assert actual == expected


def test_set_0_0_0_to_1_dirty_data():
    actual = [0, 2]
    expected = [[[1]], 2]
    set_(path[0][0][0], 1, actual)
    assert actual == expected

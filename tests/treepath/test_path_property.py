import pytest

from treepath import path, prop, Match, propm, NestedMatchNotFoundError


class PathPropertyTest:

    def __init__(self, data_):
        self._data = data_

    @property
    def data(self) -> dict:
        return self._data

    def get_data(self) -> dict:
        return self._data

    a_prop = prop(path.a, data)
    a_get = prop(path.a, get_data)
    a_b_c = prop(path.a.b.c, data, cascade=True, default=None)
    match_a_b = propm(path.a.b, data)
    match_a_b_c = propm(path.c, match_a_b)
    match_a_b_x = propm(path.x, match_a_b)

    f_0 = prop(path[0], data, default=None)
    f_0_0_0 = prop(path[0][0][0], data, cascade=True, default=None)


def test_set_a_prop_to_1_empty_data():
    actual = dict()
    expected = {"a": 1}
    ppt = PathPropertyTest(actual)
    ppt.a_prop = 1
    assert ppt.a_prop == 1
    assert actual == expected


def test_set_a_get_to_1_empty_data():
    actual = dict()
    expected = {"a": 1}
    ppt = PathPropertyTest(actual)
    ppt.a_get = 1
    assert ppt.a_get == 1
    assert actual == expected


def test_set_a_to_1_dirty_date():
    actual = {"a": 0, "x": 2}
    ppt = PathPropertyTest(actual)
    assert ppt.a_prop == 0

    expected = {"a": 1, "x": 2}
    assert ppt.a_prop == 0
    ppt.a_prop = 1
    assert actual == expected


def test_set_a_b_c_to_1_empty_data():
    actual = dict()
    expected = {"a": {"b": {"c": 1}}}
    ppt = PathPropertyTest(actual)
    assert ppt.a_b_c is None
    ppt.a_b_c = 1
    assert ppt.a_b_c == 1
    assert actual == expected


def test_set_a_b_c_to_1_dirty_data():
    actual = {"x": 2}
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    ppt = PathPropertyTest(actual)
    assert ppt.a_b_c is None
    ppt.a_b_c = 1
    assert ppt.a_b_c == 1
    assert actual == expected


def test_get_a_b_c_is_match():
    actual = {"a": {"b": {"c": 1}}, "x": 2}
    ppt = PathPropertyTest(actual)
    value = ppt.match_a_b_c
    assert isinstance(value, Match)


def test_set_a_b_x():
    actual = {"a": {"b": {"c": 1}}, "x": 2}
    expected = {"a": {"b": {"c": 1, "x": 3}}, "x": 2}
    ppt = PathPropertyTest(actual)
    with pytest.raises(NestedMatchNotFoundError):
        value = ppt.match_a_b_x

    ppt.match_a_b_x = 3
    value = ppt.match_a_b_x
    assert repr(value) == "$.a.b.x=3"
    assert actual == expected


def test_set_a_b_x_to_a_b_c():
    actual = {"a": {"b": {"c": 1}}, "x": 2}
    expected = {"a": {"b": {"c": 1, "x": 1}}, "x": 2}
    ppt = PathPropertyTest(actual)
    with pytest.raises(NestedMatchNotFoundError):
        value = ppt.match_a_b_x

    ppt.match_a_b_x = ppt.match_a_b_c
    value = ppt.match_a_b_x
    assert repr(value) == "$.a.b.x=1"
    assert actual == expected


def test_set_0_to_1_empty_data():
    actual = list()
    expected = [1]
    ppt = PathPropertyTest(actual)
    assert ppt.f_0 is None
    ppt.f_0 = 1
    assert ppt.f_0 == 1
    assert actual == expected


def test_set_0_to_1_dirty_date():
    actual = [0, 2]
    expected = [1, 2]
    ppt = PathPropertyTest(actual)
    assert ppt.f_0 == 0
    ppt.f_0 = 1
    assert ppt.f_0 == 1
    assert actual == expected


def test_set_0_0_0_to_1_empty_data():
    actual = list()
    expected = [[[1]]]
    ppt = PathPropertyTest(actual)
    assert ppt.f_0_0_0 is None
    ppt.f_0_0_0 = 1
    assert ppt.f_0_0_0 == 1
    assert actual == expected

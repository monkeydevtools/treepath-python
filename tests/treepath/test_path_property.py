from treepath import path, pprop, Match, mprop


class PathPropertyTest:

    def __init__(self, data_):
        self._data = data_

    @property
    def data(self) -> dict:
        return self._data

    def get_data(self) -> dict:
        return self._data

    a_prop = pprop(path.a, data)
    a_get = pprop(path.a, get_data)
    a_b_c = pprop(path.a.b.c, data)
    match_a_b = mprop(path.a.b, data)
    match_a_b_c = mprop(path.c, match_a_b)
    match_a_b_x = mprop(path.x, match_a_b)


    f_0 = pprop(path[0], data)
    f_0_0_0 = pprop(path[0][0][0], data)


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


def test_set_0_0_0_to_1_dirty_data():
    actual = [0, 2]
    expected = [[[1]], 2]
    ppt = PathPropertyTest(actual)
    assert ppt.f_0_0_0 == None
    ppt.f_0_0_0 = 1
    assert ppt.f_0_0_0 == 1
    assert actual == expected

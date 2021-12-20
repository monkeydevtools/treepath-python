from functools import partial

from treepath import Document, path_descriptor, path, get, set_, get_match


class PathDescriptorTest(Document):
    a = path_descriptor()
    a_b_c = path_descriptor(path.a.b.c, getter=partial(get, default=None), setter=partial(set_, cascade=True))
    match_a_b = path_descriptor(path.a.b, getter=get_match)

    f_0 = path_descriptor(path[0], getter=partial(get, default=None))
    f_0_0_0 = path_descriptor(path[0][0][0], getter=partial(get, default=None), setter=partial(set_, cascade=True))


def test_set_a_to_1_empty_data():
    actual = dict()
    expected = {"a": 1}
    ppt = PathDescriptorTest(actual)
    ppt.a = 1
    assert ppt.a == 1
    assert actual == expected


def test_set_a_to_1():
    actual = {"a": 0, "x": 2}
    expected = {"a": 1, "x": 2}

    ppt = PathDescriptorTest(actual)

    assert ppt.a == 0
    ppt.a = 1
    assert actual == expected


def test_set_a_b_c_to_1_empty_data():
    actual = dict()
    expected = {"a": {"b": {"c": 1}}}
    ppt = PathDescriptorTest(actual)
    assert ppt.a_b_c is None
    ppt.a_b_c = 1
    assert ppt.a_b_c == 1
    assert actual == expected


def test_set_a_b_c_to_1():
    actual = {"x": 2}
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    ppt = PathDescriptorTest(actual)
    assert ppt.a_b_c is None
    ppt.a_b_c = 1
    assert ppt.a_b_c == 1
    assert actual == expected


def test_set_0_to_1_empty_data():
    actual = list()
    expected = [1]
    ppt = PathDescriptorTest(actual)
    assert ppt.f_0 is None
    ppt.f_0 = 1
    assert ppt.f_0 == 1
    assert actual == expected


def test_set_0_to_1():
    actual = [0, 2]
    expected = [1, 2]
    ppt = PathDescriptorTest(actual)
    assert ppt.f_0 == 0
    ppt.f_0 = 1
    assert ppt.f_0 == 1
    assert actual == expected


def test_set_0_0_0_to_1_empty_data():
    actual = list()
    expected = [[[1]]]
    ppt = PathDescriptorTest(actual)
    assert ppt.f_0_0_0 is None
    ppt.f_0_0_0 = 1
    assert ppt.f_0_0_0 == 1
    assert actual == expected

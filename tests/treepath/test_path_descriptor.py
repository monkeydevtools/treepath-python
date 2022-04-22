from __future__ import annotations

import re
from functools import partial

import pytest

from treepath import Document, attr, attr_typed, path, get, set_, MatchNotFoundError
from treepath.path.typing.json_arg_types import JsonArgTypes


class MyDate:

    def __init__(self, *, day, month, year):
        self._day = day
        self._month = month
        self._year = year

    @staticmethod
    def to_wrapped_value(json_: JsonArgTypes) -> MyDate:
        m = re.fullmatch(r"(?P<year>[.\d]+):(?P<month>\d+):(?P<day>\d+)", json_)
        if not m:
            raise ValueError(f"Invalid value {json_} for type TestType")
        return MyDate(
            day=m.group("day"),
            month=m.group("month"),
            year=m.group("year")
        )

    @staticmethod
    def to_json_value(obj: MyDate) -> JsonArgTypes:
        return str(obj)

    def __eq__(self, other: MyDate):
        return (
                other._year == self._year and
                other._month == self._month and
                other._day == self._day
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self._year}:{self._month}:{self._day}"


def test_attr_when_empty_arg_the_get_and_set_by_attr_name():
    class PathDescriptorTest(Document):
        a = attr()

    actual = {"x": 2}
    expected = {"a": 1, "x": 2}
    pd = PathDescriptorTest(actual)
    with pytest.raises(MatchNotFoundError):
        assert pd.a != 1
    pd.a = 1
    assert pd.a == 1
    assert actual == expected


def test_attr_when_path_arg_then_get_and_set_by_attr_path():
    class PathDescriptorTest(Document):
        a = attr(path.a)
        c = attr(path.a.b.c)

    actual = {"x": 2}
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    pd = PathDescriptorTest(actual)
    with pytest.raises(MatchNotFoundError):
        assert pd.c != 1
    pd.a = {"b": {"c": 2}}
    assert pd.c == 2
    pd.c = 1
    assert pd.c == 1
    assert actual == expected


def test_attr_when_path_getter_setter_arg_then_get_and_set_by_attr_path_getter_setter():
    class PathDescriptorTest(Document):
        c = attr(path.a.b.c, getter=partial(get, default=None), setter=partial(set_, cascade=True))

    actual = {"x": 2}
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.c is None
    pd.c = 1
    assert pd.c == 1
    assert actual == expected


def test_attr_single_doc_type_transforms_on_get_and_set():
    class TestDoc(Document):
        b = attr()

    class PathDescriptorTest(Document):
        a = attr_typed(TestDoc)

    actual = {"a": {"b": 2}, "x": 2}
    expected = {"a": {"b": 1}, "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a.b == 2
    pd.a.b = 1
    assert pd.a.b == 1
    assert actual == expected


def test_attr_single_doc_type_transforms_on_partial_get_and_set():
    class TestDoc(Document):
        b = attr(getter=partial(get, default=None))

    class PathDescriptorTest(Document):
        a = attr_typed(TestDoc, getter=partial(get, default={}, store_default=True), setter=partial(set_, cascade=True))

    actual = {"x": 2}
    expected = {"a": {"b": 1}, "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a.b is None
    pd.a.b = 1
    assert pd.a.b == 1
    assert actual == expected


def test_attr_single_custom_type_transforms_on_get_and_set():

    class PathDescriptorTest(Document):
        a = attr_typed(MyDate, to_wrapped_value=MyDate.to_wrapped_value, to_json_value=MyDate.to_json_value)

    actual = {"a": "2021:05:22", "x": 2}
    expected = {"a": "2022:04:21", "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a == MyDate(year="2021", month="05", day="22")
    pd.a = MyDate(year="2022", month="04", day="21")
    assert pd.a == MyDate(year="2022", month="04", day="21")
    assert actual == expected


def test_attr_single_custom_type_transforms_on_partial_get_and_set():

    class PathDescriptorTest(Document):
        a = attr_typed(
            MyDate,
            getter=partial(get, default="2021:05:22", store_default=True),
            setter=partial(set_, cascade=True),
            to_wrapped_value=MyDate.to_wrapped_value,
            to_json_value=MyDate.to_json_value
        )

    actual = {"x": 2}
    expected = {"a": "2022:04:21", "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a == MyDate(year="2021", month="05", day="22")
    pd.a = MyDate(year="2022", month="04", day="21")
    assert pd.a == MyDate(year="2022", month="04", day="21")
    assert actual == expected

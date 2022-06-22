from __future__ import annotations

import re
from functools import partial

import pytest

from treepath import Document, attr, attr_typed, path, get, set_, MatchNotFoundError, find, SetError, wc
from treepath import JsonArgTypes
from treepath import attr_iter_typed, attr_list_typed


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
        a = attr_typed(TestDoc, getter=partial(get, default=dict, store_default=True),
                       setter=partial(set_, cascade=True))

    actual = {"x": 2}
    expected = {"a": {"b": 1}, "x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a.b is None
    pd.a.b = 1
    assert pd.a.b == 1
    assert actual == expected

    # make sure the default is a separate instance
    actual = {"x": 2}
    pd = PathDescriptorTest(actual)
    assert pd.a.b is None


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


def test_attr_iterator():
    class PathDescriptorTest(Document):
        a = attr(path.wc, getter=find)

    actual = {"a": 1, "b": 2, "c": 3}
    pd = PathDescriptorTest(actual)
    next_ = partial(next, iter(pd.a))
    assert next_() == 1
    assert next_() == 2
    assert next_() == 3

    with pytest.raises(SetError) as exc_info:
        pd.a = None

    actual = repr(exc_info.value.error_msg)
    expected = "'The path $.* does not support set.  It can only be a key or index'"
    assert actual == expected


def test_attr_iterator_doc_type_transforms_on_partial_get_and_set():
    class TestDoc(Document):
        b = attr(getter=partial(get, default=None))

    class PathDescriptorTest(Document):
        a = attr_iter_typed(TestDoc, path.wc)

    actual = {"a": {"b": 1}, "b": {"b": 2}, "c": {"b": 3}}
    pd = PathDescriptorTest(actual)
    next_ = partial(next, iter(pd.a))
    assert next_().b == 1
    assert next_().b == 2
    assert next_().b == 3

    with pytest.raises(SetError) as exc_info:
        pd.a = None

    actual = repr(exc_info.value.error_msg)
    expected = '"The iterator descriptor for path \'$.*\' does not support set"'
    assert actual == expected


def test_attr_iterator_custom_type_transforms_on_partial_get_and_set():
    class PathDescriptorTest(Document):
        a = attr_iter_typed(MyDate, path.wc.b, to_wrapped_value=MyDate.to_wrapped_value)

    actual = {"a": {"b": "2021:03:21"}, "b": {"b": "2022:04:22"}, "c": {"b": "2023:05:23"}}
    pd = PathDescriptorTest(actual)
    next_ = partial(next, iter(pd.a))
    assert next_() == MyDate(year="2021", month="03", day="21")
    assert next_() == MyDate(year="2022", month="04", day="22")
    assert next_() == MyDate(year="2023", month="05", day="23")

    with pytest.raises(SetError) as exc_info:
        pd.a = None

    actual = repr(exc_info.value.error_msg)
    expected = '"The iterator descriptor for path \'$.*.b\' does not support set"'
    assert actual == expected


def test_attr_list_doc_type_transformation():
    class TestDoc(Document):
        b = attr(getter=partial(get, default=None))

    class PathDescriptorTest(Document):
        a = attr_list_typed(TestDoc)

    actual = {"a": [{"b": 1}, {"b": 2}, {"b": 3}]}
    pd = PathDescriptorTest(actual)

    other = {"a": [{"b": 22}]}
    pd_other = PathDescriptorTest(other)

    list_wrap = pd.a

    next_ = partial(next, iter(list_wrap))
    assert next_().b == 1
    assert next_().b == 2
    assert next_().b == 3

    assert len(list_wrap) == 3

    assert list_wrap[0].b == 1
    assert list_wrap[1].b == 2
    assert list_wrap[2].b == 3

    list_wrap[0] = TestDoc({"b": 22})
    assert list_wrap[0].b == 22
    assert list_wrap[1].b == 2

    del list_wrap[0]
    assert list_wrap[0].b == 2

    assert TestDoc({"b": 22}) not in list_wrap
    assert TestDoc({"b": 3}) in list_wrap

    list_wrap.append(TestDoc({"b": 22}))
    assert TestDoc({"b": 22}) in list_wrap

    popped = list_wrap.pop(1)
    assert TestDoc({"b": 3}) not in list_wrap
    assert popped == TestDoc({"b": 3})

    def is_remove(value: TestDoc):
        return value == TestDoc({"b": 22})

    assert TestDoc({"b": 22}) in list_wrap
    list_wrap.remove_all(is_remove)
    assert TestDoc({"b": 22}) not in list_wrap

    pd.a = pd_other.a
    assert actual == other


def test_attr_list_custom_type_transformation():
    class PathDescriptorTest(Document):
        a = attr_list_typed(MyDate,
                            to_wrapped_value=MyDate.to_wrapped_value,
                            to_json_value=MyDate.to_json_value)

    actual = {"a": ["2021:03:21", "2022:04:22", "2023:05:23"]}
    pd = PathDescriptorTest(actual)

    other = {"a": ["2023:01:01"]}
    pd_other = PathDescriptorTest(other)

    list_wrap = pd.a

    next_ = partial(next, iter(list_wrap))
    assert next_() == MyDate(year="2021", month="03", day="21")
    assert next_() == MyDate(year="2022", month="04", day="22")
    assert next_() == MyDate(year="2023", month="05", day="23")

    assert len(list_wrap) == 3

    assert list_wrap[0] == MyDate(year="2021", month="03", day="21")
    assert list_wrap[1] == MyDate(year="2022", month="04", day="22")
    assert list_wrap[2] == MyDate(year="2023", month="05", day="23")

    list_wrap[0] = MyDate(year="2000", month="01", day="01")
    assert list_wrap[0] == MyDate(year="2000", month="01", day="01")
    assert list_wrap[1] == MyDate(year="2022", month="04", day="22")

    del list_wrap[0]
    assert list_wrap[0] == MyDate(year="2022", month="04", day="22")

    assert MyDate(year="2000", month="01", day="01") not in list_wrap
    assert MyDate(year="2022", month="04", day="22") in list_wrap

    list_wrap.append(MyDate(year="2022", month="04", day="22"))
    assert MyDate(year="2022", month="04", day="22") in list_wrap

    popped = list_wrap.pop(1)
    assert MyDate(year="2023", month="05", day="23") not in list_wrap
    assert popped == MyDate(year="2023", month="05", day="23")

    def is_remove(value: MyDate):
        return value == MyDate(year="2022", month="04", day="22")

    assert MyDate(year="2022", month="04", day="22") in list_wrap
    list_wrap.remove_all(is_remove)
    assert MyDate(year="2022", month="04", day="22") not in list_wrap

    pd.a = pd_other.a
    assert actual == other


def test_value_error_when_class_not_document():
    with pytest.raises(RuntimeError) as exc_info:
        class SomeClass:
            a = attr()

    actual = repr(exc_info.value)
    expected = ('RuntimeError("Error calling __set_name__ on \'PathDescriptor\' instance \'a\' in \'SomeClass\'")')
    assert actual == expected


def test_return_self_when_not_instance():
    descriptor = attr()

    class SomeClass(Document):
        a = descriptor

    assert descriptor is SomeClass.a


def test_descript_function_attr_example():
    class X(Document):
        a = attr()

    x = X({"a": 1})
    assert x.a == 1


def test_descript_function_attr_typed_example():
    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_typed(X)

    y = Y({"b": {"a": 1}})
    assert y.b.a == 1


def test_descript_function_attr_iter_typed_example():
    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_iter_typed(X, path.b[wc])

    y = Y({"b": [{"a": 1}, {"a": 2}]})
    x = iter(y.b)
    assert next(x).a == 1
    assert next(x).a == 2


def test_descript_function_attr_list_typed_example():
    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_list_typed(X, path.b)

    y = Y({"b": [{"a": 1}, {"a": 2}]})

    assert y.b[0].a == 1
    assert y.b[1].a == 2

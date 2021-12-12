import pytest

from treepath import path, pop, PopError, wc, has, MatchNotFoundError, pop_match, get_match
from treepath.path.builder.path_builder import get_vertex_from_path_builder
from treepath.path.traverser.match_traverser import MatchTraverser


def test_set_a_to_1_invalid_type():
    expected = "PopError(Invalid pop data[0] because data is of type: <class \'dict\'>, expecting " \
               "type: <class \'list\'>\n" \
               "  path: $[0])"""
    data = {"a": 1}
    with pytest.raises(PopError) as exc_info:
        match = get_match(path.a, data)
        vertex = get_vertex_from_path_builder(path[0])
        MatchTraverser.pop(match, vertex)
    actual = repr(exc_info.value)
    assert actual == expected


def test_set_0_to_a_invalid_type():
    expected = "PopError(Invalid pop data['a'] because data is of type: <class \'list\'>, expecting " \
               "type: <class \'dict\'>\n" \
               "  path: $.a)"""
    data = [0]
    with pytest.raises(PopError) as exc_info:
        match = get_match(path[0], data)
        vertex = get_vertex_from_path_builder(path.a)
        MatchTraverser.pop(match, vertex)
    actual = repr(exc_info.value)
    assert actual == expected


def test_pop_wc_invalid_path():
    expected = "PopError(The path $[*] does not support pop.  It can only be a key or index\n  path: $[*])"
    data = [0, 1]
    with pytest.raises(PopError) as exc_info:
        pop(path[wc], data)
    assert repr(exc_info.value) == expected


def test_pop_a():
    actual = {"a": 1, "x": 2}
    expected_return = 1
    expected = {"x": 2}
    actual_return = pop(path.a, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_a_b_c():
    actual = {"a": {"b": {"c": 1}}}
    expected_return = 1
    expected = {"a": {"b": {}}}
    actual_return = pop(path.a.b.c, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_a_predicate():
    actual = {"a": 0, "x": 2}
    expected_return = 0
    expected = {"x": 2}
    actual_return = pop(path[has(path.a == 0)].a, actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_match_a_predicate():
    actual = {"a": 0, "x": 2}
    expected_return = '$.a=0'
    expected = {"x": 2}
    actual_return = pop_match(path[has(path.a == 0)].a, actual)
    assert actual == expected
    assert repr(actual_return) == expected_return


def test_pop_a_predicate_match_not_found():
    actual = {"a": 0, "x": 2}
    expected_error_message = 'MatchNotFoundError(No get_match occurred on path: $[has($.a == 1)].a)'
    expected = {"a": 0, "x": 2}
    with pytest.raises(MatchNotFoundError) as exc_info:
        pop(path[has(path.a == 1)].a, actual)
    assert actual == expected
    assert repr(exc_info.value) == expected_error_message


def test_pop_a_predicate_default():
    actual = {"a": 0, "x": 2}
    expected_return = 0
    expected = {"a": 0, "x": 2}
    actual_return = pop(path[has(path.a == 1)].a, actual, default=0)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_0():
    actual = [1, 2]
    expected_return = 1
    expected = [2]
    actual_return = pop(path[0], actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_0_1_2():
    actual = [[[1]]]
    expected_return = 1
    expected = [[[]]]
    actual_return = pop(path[0][0][0], actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_0_predicate():
    actual = [1, 2]
    expected_return = 1
    expected = [2]
    actual_return = pop(path[has(path[0] == 1)][0], actual)
    assert actual == expected
    assert actual_return == expected_return


def test_pop_match_0_predicate():
    actual = [1, 2]
    expected_return = '$[0]=1'
    expected = [2]
    actual_return = pop_match(path[has(path[0] == 1)][0], actual)
    assert actual == expected
    assert repr(actual_return) == expected_return


def test_pop_0_predicate_match_not_found():
    actual = [1, 2]
    expected_error_message = 'MatchNotFoundError(No get_match occurred on path: $[has($.a == 1)].a)'
    expected = [1, 2]
    with pytest.raises(MatchNotFoundError) as exc_info:
        pop(path[has(path.a == 1)].a, actual)
    assert actual == expected
    assert repr(exc_info.value) == expected_error_message


def test_pop_0_predicate_default():
    actual = [1, 2]
    expected_return = 0
    expected = [1, 2]
    actual_return = pop(path[has(path.a == 1)].a, actual, default=0)
    assert actual == expected
    assert actual_return == expected_return

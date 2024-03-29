from tests.utils.traverser_utils import *
from treepath import get, path, get_match, pathd
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_dash_x_as_string(dash):
    expected = dash["-x"]
    actual = get(path["-x"], dash)
    assert actual == expected


def test_dash_x_as_string_path(dash):
    expected = dash["-x"]
    actual = get_match(path["-x"], dash)
    assert repr(actual) == f"$.-x={expected}"


def test_dash_x_as_syntax(dash):
    expected = dash["-x"]
    actual = get(pathd._x, dash)
    assert actual == expected


def test_dash_x_as_syntax_path(dash):
    expected = dash["-x"]
    actual = get_match(pathd._x, dash)
    assert repr(actual) == f"$.-x={expected}"


def test_dash_x_x_as_syntax(dash):
    expected = dash["-x"]["-x-"]
    actual = get(pathd._x._x_, dash)
    assert actual == expected


def test_dash_x_x_x_as_syntax(dash):
    expected = dash["-x"]["-x-"]["-x-x-"]
    actual = get(pathd._x._x_._x_x_, dash)
    assert actual == expected


def test_underscore_y_y_y_as_syntax(dash):
    expected = dash["-x"]["-x-"]["_y_y_"]
    actual = get(pathd._x._x_["_y_y_"], dash)
    assert actual == expected


def test_underscore_y_y_y_as_syntax_MatchNotFoundError(dash):
    with pytest.raises(MatchNotFoundError):
        get(pathd._x._x_._y_y_, dash)

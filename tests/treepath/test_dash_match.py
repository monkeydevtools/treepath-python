from tests.utils.traverser_utils import *
from treepath import get, exp, match, expd
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_dash_x_as_string(dash):
    expected = dash["-x"]
    actual = get(exp["-x"], dash)
    assert actual == expected


def test_dash_x_as_string_path(dash):
    expected = dash["-x"]
    actual = match(exp["-x"], dash)
    assert repr(actual) == f"$.-x={expected}"


def test_dash_x_as_syntax(dash):
    expected = dash["-x"]
    actual = get(expd._x, dash)
    assert actual == expected


def test_dash_x_as_syntax_path(dash):
    expected = dash["-x"]
    actual = match(expd._x, dash)
    assert repr(actual) == f"$.-x={expected}"


def test_dash_x_x_as_syntax(dash):
    expected = dash["-x"]["-x-"]
    actual = get(expd._x._x_, dash)
    assert actual == expected


def test_dash_x_x_x_as_syntax(dash):
    expected = dash["-x"]["-x-"]["-x-x-"]
    actual = get(expd._x._x_._x_x_, dash)
    assert actual == expected


def test_underscore_y_y_y_as_syntax(dash):
    expected = dash["-x"]["-x-"]["_y_y_"]
    actual = get(expd._x._x_["_y_y_"], dash)
    assert actual == expected


def test_underscore_y_y_y_as_syntax_MatchNotFoundError(dash):
    with pytest.raises(MatchNotFoundError):
        get(expd._x._x_._y_y_, dash)

import os

import pytest

from treepath import path
from treepath.path.exceptions.path_syntax_error import PathSyntaxError


def test_PathSyntaxError_on_invalid_indices():
    expected = "PathSyntaxError(Unsupported indices: [<class 'float'>].  Indices must be either an int, " \
               "slice, tuple, str, wildcard, has(function), or callable." \
               f"{os.linesep}" \
               "  path: $.a[1.0])"
    with pytest.raises(PathSyntaxError) as exc_info:
        b = path.a[1.0]

    assert repr(exc_info.value) == expected


def test_AttributeError_on_indices_assignment():
    expected = "AttributeError('set __setitem__  0 not supported on $.__name__',)"
    with pytest.raises(AttributeError) as exc_info:
        path[0] = 1

    assert repr(exc_info.value) == expected


def test_AttributeError_on_attr_assignment():
    expected = "AttributeError('set __setattr__  a 1 not supported on $.__name__',)"
    with pytest.raises(AttributeError) as exc_info:
        path.a = 1

    assert repr(exc_info.value) == expected


def test_path_repr_eq_str():
    some_path = path.x.y[0]
    assert repr(some_path) == str(some_path)


def test_PathSyntaxError_on_double_rec():
    expected = f"PathSyntaxError(Successive recursive vertices are not allowed in the path expression.{os.linesep}" \
               "  path: $..recursive)"
    with pytest.raises(PathSyntaxError) as exc_info:
        b = path.rec.rec

    assert repr(exc_info.value) == expected

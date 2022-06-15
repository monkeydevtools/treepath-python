import os

import pytest

from treepath import path, get, TraversingError, get_match
from treepath.path.exceptions.path_syntax_error import PathSyntaxError


def test_vertex_tuple_repr():
    expected = "$[1, 2]"
    assert repr(path[1, 2]) == expected


def test_vertex_parent_repr():
    expected = "$.x.x.parent"
    assert repr(path.x.x.parent) == expected


def test_vertex_slice_does_not_iterate_dict(keys):
    expected = None
    actual = get(path.x[:1], keys, default=None)
    assert actual == expected


def test_vertex_tuple_invalid_for_dict(keys):
    expected = None
    actual = get(path.x.x.x[1, 2], keys, default=None)
    assert actual == expected


def test_vertex_TraversingError_root_cannot_be_traverse():
    expected = f"TraversingError(Possible Bug.  The root match method should never be called.{os.linesep}" \
               f"  path: ${os.linesep}" \
               "  last_match: $={})"
    with pytest.raises(TraversingError) as exc_info:
        actual = get_match(path, {})
        # the root match method should never be called.
        # but in case of a bug, make sure it creates a error
        actual._traverser_match.vertex.match(actual._traverser_match, traverser=None, vertex_index=0)

    assert repr(exc_info.value) == expected


def test_vertex_PathSyntaxError_tuple_invalid_comma_seperated_indices():
    expected = "PathSyntaxError(Unsupported indices: [0, '1', 1.0].  Comma serrated indices can be a combination of " \
               f"int and str values.{os.linesep}" \
               "  path: $.a[0, '1', 1.0])"
    with pytest.raises(PathSyntaxError) as exc_info:
        b = path.a[0, '1', 1.0]

    assert repr(exc_info.value) == expected

import os

import pytest

from treepath import path, get, get_match, find
from treepath.path.exceptions.infinite_loop_detected import InfiniteLoopDetected
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.exceptions.nested_match_not_found_error import NestedMatchNotFoundError
from treepath.path.exceptions.stop_traversing import StopTraversing
from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.exceptions.treepath_exception import TreepathException


def test_TreepathException_no_double_resolve(keys):
    expected = f"TreepathException(path: $.x)"
    with pytest.raises(TreepathException) as exc_info:
        raise TreepathException(path.x)

    repr(exc_info.value)
    assert str(exc_info.value) == expected
    assert exc_info.value.is_msg_resolved


def test_MatchNotFoundError_validate_message(keys):
    expected = "MatchNotFoundError(No get_match occurred on path: $.a)"
    with pytest.raises(MatchNotFoundError) as exc_info:
        get(path.a, keys)

    assert repr(exc_info.value) == expected


def test_NestedMatchNotFoundError_validate_message(keys):
    expected = "NestedMatchNotFoundError(No get_match occurred on path $.a from match $.x)"
    with pytest.raises(NestedMatchNotFoundError) as exc_info:
        get(path.a, get_match(path.x, keys))

    assert repr(exc_info.value) == expected


def test_StopTraversing_validate_message(keys):
    expected = "StopTraversing(Traversing has completed on path: $.a)"
    with pytest.raises(StopTraversing) as exc_info:
        next(find(path.a, keys))

    assert repr(exc_info.value) == expected


def test_TraversingError_validate_message(keys):
    expected = f"TraversingError(Evaluation of predicate failed because of error: NotImplementedError(){os.linesep}" \
               f"  path: $.x.x.x{os.linesep}" \
               f"  last_match: $.x.x.x=1)"
    with pytest.raises(TraversingError) as exc_info:
        def crap(*args):
            raise NotImplementedError

        next(find(path.x.x.x[crap], keys))

    assert repr(exc_info.value) == expected


def test_InfiniteLoopDetected_validate_message():
    expected = 'InfiniteLoopDetected(Traversing seems to go on for ever on path: $..)'

    one = {}
    two = {}
    one["x"] = two
    two["x"] = one

    with pytest.raises(InfiniteLoopDetected) as exc_info:
        get(path.rec.a, one)

    assert repr(exc_info.value) == expected

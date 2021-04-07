from typing import Union, Iterator, Callable, Any

from treepath.path.builder.path_builder import PathBuilder, get_vertex_from_path_builder
from treepath.path.builder.path_builder_predicate import PathBuilderPredicate
from treepath.path.builder.path_predicate import PathPredicate
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.exceptions.nested_match_not_found_error import NestedMatchNotFoundError
from treepath.path.traverser.has_function import create_has_predicate
from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser
from treepath.path.traverser.nested_value_traverser import NestedValueTraverser
from treepath.path.traverser.predicate_match import PredicateMatch
from treepath.path.traverser.trace import Trace
from treepath.path.traverser.value_traverser import ValueTraverser
from treepath.path.util.decorator import pretty_repr, add_attr

_not_set = dict()


def get(
        expression: PathBuilder,
        data: Union[dict, list, Match],
        default=_not_set,
        trace: Callable[[Trace], None] = None
) -> Union[dict, list, str, int, float, bool, None]:
    """

    """
    must_match = (default is _not_set)
    match = get_match(expression, data, must_match=must_match, trace=trace)
    if match:
        return match.data
    return default


def find(
        expression: PathBuilder,
        data: Union[dict, list, Match],
        trace: Callable[[Trace], None] = None
) -> Iterator[Union[dict, list, str, int, float, bool, None]]:
    """

    """
    if isinstance(data, Match):
        return nested_find(expression, data, trace=trace)

    vertex = get_vertex_from_path_builder(expression)
    traverser = ValueTraverser(data, vertex, trace=trace)
    traverser_iter = iter(traverser)
    return traverser_iter


def get_match(
        expression: PathBuilder,
        data: Union[dict, list, Match],
        must_match: bool = True,
        trace: Callable[[Trace], None] = None
) -> Union[Match, None]:
    """

    """
    if isinstance(data, Match):
        return nested_get_match(expression, data, must_match=must_match, trace=trace)

    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex, trace=trace)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        pass
    if must_match:
        raise MatchNotFoundError(vertex)
    return None


def find_matches(
        expression: PathBuilder,
        data: Union[dict, list, Match],
        trace: Callable[[Trace], None] = None
) -> Iterator[Match]:
    """

    """
    if isinstance(data, Match):
        return nested_find_matches(expression, data, trace=trace)

    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex, trace=trace)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_find(
        expression: PathBuilder,
        parent_match: Match,
        trace: Callable[[Trace], None] = None
) -> Iterator[Union[dict, list, str, int, float, bool, None]]:
    """

    """
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedValueTraverser(parent_match._traverser_match, vertex, trace=trace)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_get_match(
        expression: PathBuilder,
        parent_match: Match,
        must_match: bool = True,
        trace: Callable[[Trace], None] = None
) -> Union[Match, None]:
    """

    """
    if isinstance(parent_match, PredicateMatch):
        trace = parent_match.trace

    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex, trace=trace)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        pass
    if must_match:
        raise NestedMatchNotFoundError(parent_match, vertex)
    return None


def nested_find_matches(
        expression: PathBuilder,
        parent_match: Match,
        trace: Callable[[Trace], None] = None
) -> Iterator[Match]:
    """

    """
    if isinstance(parent_match, PredicateMatch):
        trace = parent_match.trace
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex, trace=trace)
    traverser_iter = iter(traverser)
    return traverser_iter


def has_args(*args):
    """

    """
    def process_arg(arg):
        if isinstance(arg, tuple):
            return create_has_predicate(nested_find_matches, *arg)
        else:
            return create_has_predicate(nested_find_matches, arg)

    has_predicates = [process_arg(arg) for arg in args]

    def wrap(function):
        @pretty_repr(
            lambda: f"{', '.join(map(repr, has_predicates))}")
        def predicate(parent_match):
            return function(parent_match, *has_predicates)

        return predicate

    return wrap


@add_attr("args", has_args)
def has(
        path: Union[PathBuilderPredicate, PathPredicate],
        *single_arg_functions: [Callable[[Any], Any]]) -> Callable[[Match], Any]:
    """

    """
    return create_has_predicate(nested_find_matches, path, *single_arg_functions)

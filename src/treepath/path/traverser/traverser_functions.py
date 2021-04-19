from typing import Union, Iterator, Callable, Any, Tuple

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

_has_typing_first_arg = Union[
    PathBuilderPredicate,
    PathPredicate,
    Callable[[Match], Any]
]
_has_typing_single_arg_functions = Callable[[Any], Any]

_has_tuple_arg_type = Tuple[
    _has_typing_first_arg,
    _has_typing_single_arg_functions,
]

_has_multiple_arg_type = Union[
    _has_typing_first_arg,
    _has_tuple_arg_type,
]

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


def has_these(*args: _has_multiple_arg_type, repr_join_key=', '):
    """

    """

    def process_has_arg(arg):
        if isinstance(arg, tuple):
            return create_has_predicate(nested_find_matches, *arg)
        else:
            return create_has_predicate(nested_find_matches, arg)

    has_predicates = [process_has_arg(arg) for arg in args]

    def wrap(function):
        @pretty_repr(lambda: f"{repr_join_key.join(map(repr, has_predicates))}")
        def predicate(parent_match):
            return function(parent_match, *has_predicates)

        return predicate

    return wrap


def has_all(*args: _has_multiple_arg_type):
    """
    Tuple[Union[PathBuilderPredicate, PathPredicate, Callable[[Match], Any]]]
    """

    @has.these(*args, repr_join_key=' and ')
    def and_predicate(parent_match: Match, *predicates) -> Any:
        for predicate in predicates:
            if not predicate(parent_match):
                return False
        return True

    return and_predicate


def has_any(*args: _has_multiple_arg_type):
    """

    """

    @has.these(*args, repr_join_key=' or ')
    def or_predicate(parent_match: Match, *predicates) -> Any:
        for predicate in predicates:
            if predicate(parent_match):
                return True
        return False

    return or_predicate


def has_not(
        path: _has_typing_first_arg,
        *single_arg_functions: _has_typing_single_arg_functions) -> Callable[[Match], Any]:
    """
    Tuple[Union[PathBuilderPredicate, PathPredicate, Callable[[Match], Any]]]
    """

    predicate = create_has_predicate(nested_find_matches, path, *single_arg_functions)

    def not_predicate(parent_match: Match) -> Any:
        return not predicate(parent_match)

    return not_predicate


@add_attr("these", has_these)
def has(
        path: _has_typing_first_arg,
        *single_arg_functions: _has_typing_single_arg_functions) -> Callable[[Match], Any]:
    """

    """
    return create_has_predicate(nested_find_matches, path, *single_arg_functions)

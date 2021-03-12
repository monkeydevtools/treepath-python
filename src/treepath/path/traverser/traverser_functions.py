import functools
from typing import Union, Iterator, Callable, Any

from treepath.path.builder.path_builder import PathBuilder, get_vertex_from_path_builder
from treepath.path.builder.path_builder_predicate import PathBuilderPredicate
from treepath.path.builder.path_predicate import PathPredicate
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser
from treepath.path.traverser.nested_value_traverser import NestedValueTraverser
from treepath.path.traverser.value_traverser import ValueTraverser
from treepath.path.util.decorator import pretty_rep
from treepath.path.util.function import tuple_iterable

_not_set = dict()


def get(expression: PathBuilder, data: Union[dict, list, Match], default=_not_set
        ) -> Union[dict, list, str, int, float, bool, None]:
    must_match = (default is _not_set)
    match = get_match(expression, data, must_match=must_match)
    if match:
        return match.data
    return default


def find(expression: PathBuilder, data: Union[dict, list, Match]) -> Iterator[
    Union[dict, list, str, int, float, bool, None]]:
    if isinstance(data, Match):
        return nested_find(expression, data)

    vertex = get_vertex_from_path_builder(expression)
    traverser = ValueTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def get_match(expression: PathBuilder, data: Union[dict, list, Match], must_match: bool = True) -> Union[Match, None]:
    if isinstance(data, Match):
        return nested_get_match(expression, data, must_match)

    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        pass
    if must_match:
        raise MatchNotFoundError(vertex)
    return None


def find_matches(expression: PathBuilder, data: Union[dict, list, Match]) -> Iterator[Match]:
    if isinstance(data, Match):
        return nested_find_matches(expression, data)

    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_find(expression: PathBuilder, parent_match: Match) -> Iterator[
    Union[dict, list, str, int, float, bool, None]]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedValueTraverser(parent_match._traverser_match, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_get_match(expression: PathBuilder, parent_match: Match, must_match: bool = True) -> Union[Match, None]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        pass
    if must_match:
        raise MatchNotFoundError(vertex)
    return None


def nested_find_matches(expression: PathBuilder, parent_match: Match) -> Iterator[Match]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def has(
        path: Union[PathBuilderPredicate, PathPredicate],
        *single_arg_functions: [Callable[[Any], Any]]) -> Callable[[Match], Any]:
    if isinstance(path, PathPredicate):
        real_path = path.path
        single_arg_operation = path.operation
    else:
        real_path = path
        single_arg_operation = None

    match_iter = functools.partial(nested_find_matches, real_path)

    if single_arg_operation and single_arg_functions:
        @pretty_rep(
            lambda: f"has({real_path} {single_arg_operation}, {', '.join(tuple_iterable(single_arg_functions))})")
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):

                value = next_match.data
                for function in single_arg_functions[::-1]:
                    value = function(value)

                value = single_arg_operation(value)

                if value:
                    return True
            return False

        return has_predicate

    if not single_arg_operation and single_arg_functions:
        @pretty_rep(lambda: f"has({real_path}, {', '.join(tuple_iterable(single_arg_functions))})")
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):

                value = next_match.data
                for function in single_arg_functions[::-1]:
                    value = function(value)

                if value:
                    return True
            return False

        return has_predicate

    if single_arg_operation and not single_arg_functions:
        @pretty_rep(lambda: f"has({real_path} {single_arg_operation})")
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):
                value = single_arg_operation(next_match.data)
                if value:
                    return True
            return False

        return has_predicate

    else:
        @pretty_rep(lambda: f"has({real_path})")
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):
                return True
            return False

        return has_predicate

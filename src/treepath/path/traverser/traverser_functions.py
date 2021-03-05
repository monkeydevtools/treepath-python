import functools
import operator
from typing import Union, Iterator, Callable, Any

from treepath.path.builder.path_builder import PathBuilder, get_vertex_from_path_builder
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser
from treepath.path.traverser.value_traverser import ValueTraverser
from treepath.path.util.decorator import do_nothing

_not_set = dict()


def get(expression: PathBuilder, data: Union[dict, list], default=_not_set
        ) -> Union[dict, list, str, int, float, bool, None]:
    must_match = (default is _not_set)
    match = get_match(expression, data, must_match=must_match)
    if match:
        return match.data
    return default


def find(expression: PathBuilder, data: Union[dict, list]) -> Iterator[Union[dict, list, str, int, float, bool, None]]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = ValueTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def get_match(expression: PathBuilder, data: Union[dict, list], must_match: bool = True) -> Union[Match, None]:
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



def find_matches(expression: PathBuilder, data: Union[dict, list]) -> Iterator[Match]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
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


def _has(has_func):
    """
    A decorator for unpacking a tuple that might be hidden in first arg
    """

    def _unpack(*args):
        first_arg = args[0]
        path = first_arg
        new_args = []
        if isinstance(first_arg, tuple):
            path = first_arg[0]
            hidden_single_arg_function = first_arg[1]
            new_args.append(hidden_single_arg_function)
        for single_arg_function  in args[1:]:
            new_args.append(single_arg_function)
        return has_func(path, *new_args)
    return _unpack


@_has
def has(path: PathBuilder, *single_arg_function: [Callable[[Any], Any]]) -> Callable[[Match], Any]:
    match_iter = functools.partial(nested_find_matches, path)

    def create_has_predicate():
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):
                if len(single_arg_function) == 0:
                    return True

                value = next_match.data
                for function in single_arg_function[::-1]:
                    value = function(value)
                if value:
                    return True
            return False

        return has_predicate

    return create_has_predicate()

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


def get(expression: PathBuilder, data: Union[dict, list], must_match: bool = True
        ) -> Union[dict, list, str, int, float, bool, None]:
    return get_match(expression, data, must_match=must_match).data


def find(expression: PathBuilder, data: Union[dict, list]) -> Iterator[Any]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = ValueTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def _has(has_func):
    """
    A decorator for has to allow for dynamic args
    (expression, operator_, convert_type)
    (expression, operator_, )
    (expression)
    ((expression, operator_), convert_type) maps to (expression, operator_, convert_type)
    ((expression, operator_)) maps to (expression, operator_)
    """

    def _unpack(*args):
        outer_length = len(args)
        first_arg = args[0]
        expression = first_arg
        single_arg_operator = operator.truth
        single_arg_convert_type = do_nothing
        if outer_length > 1:
            single_arg_operator = args[1]
            single_arg_convert_type = single_arg_operator
        if isinstance(first_arg, tuple):
            expression = first_arg[0]
            single_arg_operator = first_arg[1]
        if outer_length > 2:
            single_arg_convert_type = args[2]

        return has_func(expression, single_arg_operator, single_arg_convert_type)

    return _unpack


@_has
def has(
        expression: PathBuilder,
        single_arg_operator: Callable[[Any], bool],
        single_arg_convert_type: Callable[[Any], Any]) -> Callable[[Match], Any]:
    match_iter = functools.partial(nested_match_all, expression)

    def create_has_predicate():
        def has_predicate(parent_match: Match):
            for next_match in match_iter(parent_match):
                if single_arg_operator(single_arg_convert_type(next_match.data)):
                    return True
            return False

        return has_predicate

    return create_has_predicate()


def get_match(expression: PathBuilder, data: Union[dict, list], must_match: bool = True) -> Union[Match, None]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        if must_match:
            raise MatchNotFoundError(vertex)
        return None


def find_matches(expression: PathBuilder, data: Union[dict, list]) -> Iterator[Match]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_match_all(expression: PathBuilder, parent_match: Match) -> Iterator[Match]:
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter

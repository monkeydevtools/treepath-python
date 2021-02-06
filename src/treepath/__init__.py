import functools
import operator

from treepath.path.builder.dash_path_builder import DashRoot
from treepath.path.builder.patch_constants import *
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.builder.path_builder import PathBuilder, get_vertex_from_path_builder
from treepath.path.builder.root_path_builder import Root
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser
from treepath.path.traverser.value_traverser import ValueTraverser
from treepath.path.util.decorator import do_nothing

exp = Root()
expd = DashRoot()


def get(expression: PathBuilder, data):
    return match(expression, data).data


def find(expression: PathBuilder, data):
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
def has(expression, single_arg_operator, single_arg_convert_type):
    match_iter = functools.partial(nested_match, expression)

    def create_has_predicate():
        def has_predicate(parent_match: Match):
            next_match = match_iter(parent_match)
            if next_match:
                return single_arg_operator(single_arg_convert_type(next_match.data))
            else:
                return single_arg_operator(None)

        return has_predicate

    return create_has_predicate()


def and_(*predicates):
    def create_and_predicate():
        def and_predicate(parent_match: Match):
            for predicate in predicates:
                if not predicate(parent_match):
                    return False

            return True

        return and_predicate

    return create_and_predicate()


def or_(*predicates):
    def create_or_predicate():
        def or_predicate(parent_match: Match):
            for predicate in predicates:
                if predicate(parent_match):
                    return True
            return False

        return or_predicate

    return create_or_predicate()


def match(expression: PathBuilder, data) -> Match:
    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        raise MatchNotFoundError(vertex)


def match_all(expression: PathBuilder, data):
    vertex = get_vertex_from_path_builder(expression)
    traverser = MatchTraverser(data, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter


def nested_match(expression: PathBuilder, parent_match: Match) -> Match:
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match, vertex)
    traverser_iter = iter(traverser)
    try:
        return next(traverser_iter)
    except StopIteration:
        pass


def nested_match_all(expression: PathBuilder, parent_match: Match):
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match, vertex)
    traverser_iter = iter(traverser)
    return traverser_iter

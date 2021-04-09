import functools
from typing import Union, Callable, Any

from treepath.path.builder.path_builder_predicate import PathBuilderPredicate
from treepath.path.builder.path_predicate import PathPredicate
from treepath.path.exceptions.path_syntax_error import PathSyntaxError
from treepath.path.traverser.match import Match
from treepath.path.util.decorator import pretty_repr


def create_has_predicate(
        nested_find_matches,
        path: Union[PathBuilderPredicate, PathPredicate,  Callable[[Match], Any]],
        *value_remap: [Callable[[Any], Any]]) -> Callable[[Match], Any]:
    if isinstance(path, PathPredicate):
        real_path = path.path
        single_arg_operator = path.operation
    elif isinstance(path, PathBuilderPredicate):
        real_path = path
        single_arg_operator = None
    elif isinstance(path, Callable):
        return path
    else:
        raise PathSyntaxError(
            parent_vertex=None,
            error_msg=f"Invalid  path [{type(path)}] argument.   Expecting PathBuilderPredicate, PathPredicate,  or "
                      'Callable[[Match], Any]]',
            invalid_path_segment='')

    match_iter = functools.partial(nested_find_matches, real_path)

    if single_arg_operator and value_remap:
        return _create_has_predicate_with_single_arg_operator_and_value_remap(
            real_path,
            match_iter,
            single_arg_operator,
            value_remap
        )

    if not single_arg_operator and value_remap:
        return _create_has_predicate_with_value_remap(real_path, match_iter, value_remap)

    if single_arg_operator and not value_remap:
        return _create_has_predicate_with_single_arg_operator(real_path, match_iter, single_arg_operator)
    else:
        return _create_has_predicate(real_path, match_iter)


def _create_has_predicate_with_single_arg_operator_and_value_remap(
        real_path,
        match_iter,
        single_arg_operator,
        value_remap
):
    @pretty_repr(
        lambda: f"has({real_path} {single_arg_operator}, {', '.join(map(repr, value_remap))})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):

            value = next_match.data
            for function in value_remap[::-1]:
                value = function(value)

            value = single_arg_operator(value)

            if value:
                return True
        return False

    return has_predicate


def _create_has_predicate_with_value_remap(real_path, match_iter, value_remap):
    @pretty_repr(lambda: f"has({real_path}, {', '.join(map(repr, value_remap))})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):

            value = next_match.data
            for function in value_remap[::-1]:
                value = function(value)

            if value:
                return True
        return False

    return has_predicate


def _create_has_predicate_with_single_arg_operator(real_path, match_iter, single_arg_operator):
    @pretty_repr(lambda: f"has({real_path} {single_arg_operator})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):
            value = single_arg_operator(next_match.data)
            if value:
                return True
        return False

    return has_predicate


def _create_has_predicate(real_path, match_iter):
    @pretty_repr(lambda: f"has({real_path})")
    def has_predicate(parent_match: Match):
        for _ in match_iter(parent_match):
            return True
        return False

    return has_predicate

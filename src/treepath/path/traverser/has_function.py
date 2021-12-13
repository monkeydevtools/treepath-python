import functools
from typing import Union, Callable, Any

from treepath.path.builder.path_builder_predicate import PathBuilderPredicate
from treepath.path.builder.path_predicate import PathPredicate
from treepath.path.exceptions.path_syntax_error import PathSyntaxError
from treepath.path.traverser.match import Match
from treepath.path.utils.decorator import pretty_repr


def create_has_predicate(
        nested_find_matches,
        path: Union[PathBuilderPredicate, PathPredicate, Callable[[Match], Any]],
        *single_arg_functions: [Callable[[Any], Any]]) -> Callable[[Match], Any]:
    if isinstance(path, PathPredicate):
        real_path = path.path
        path_predicate_operation = path.operation
    elif isinstance(path, PathBuilderPredicate):
        real_path = path
        path_predicate_operation = None
    elif isinstance(path, Callable):
        return path
    else:
        raise PathSyntaxError(
            parent_vertex=None,
            error_msg=f"Invalid  path [{type(path)}] argument.   Expecting PathBuilderPredicate, PathPredicate,  or "
                      'Callable[[Match], Any]]',
            invalid_path_segment='')

    match_iter = functools.partial(nested_find_matches, real_path)

    if path_predicate_operation and single_arg_functions:
        return _create_has_predicate_with_path_predicate_operation_and_single_arg_functions(
            real_path,
            match_iter,
            path_predicate_operation,
            single_arg_functions
        )

    if not path_predicate_operation and single_arg_functions:
        return _create_has_predicate_with_single_arg_functions(real_path, match_iter, single_arg_functions)

    if path_predicate_operation and not single_arg_functions:
        return _create_has_predicate_with_path_predicate_operation(real_path, match_iter, path_predicate_operation)
    else:
        return _create_has_predicate(real_path, match_iter)


def _create_has_predicate_with_path_predicate_operation_and_single_arg_functions(
        real_path,
        match_iter,
        path_predicate_operation,
        single_arg_functions
):
    @pretty_repr(
        lambda: f"has({real_path} {path_predicate_operation}, {', '.join(map(repr, single_arg_functions))})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):

            value = next_match.data
            for function in single_arg_functions[::-1]:
                value = function(value)

            value = path_predicate_operation(value)

            if value:
                return True
        return False

    return has_predicate


def _create_has_predicate_with_single_arg_functions(real_path, match_iter, single_arg_functions):
    @pretty_repr(lambda: f"has({real_path}, {', '.join(map(repr, single_arg_functions))})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):

            value = next_match.data
            for function in single_arg_functions[::-1]:
                value = function(value)

            if value:
                return True
        return False

    return has_predicate


def _create_has_predicate_with_path_predicate_operation(real_path, match_iter, path_predicate_operation):
    @pretty_repr(lambda: f"has({real_path} {path_predicate_operation})")
    def has_predicate(parent_match: Match):
        for next_match in match_iter(parent_match):
            value = path_predicate_operation(next_match.data)
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

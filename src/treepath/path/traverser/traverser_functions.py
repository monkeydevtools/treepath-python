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

# The value used to indicate an argument is not set.
_not_set = dict()


def get(
        expression: PathBuilder,
        data: Union[dict, list, Match],
        default=_not_set,
        trace: Callable[[Trace], None] = None
) -> Union[dict, list, str, int, float, bool, None]:
    """
    Returns the first value in the data that satisfies the path expression.   When no result is found, a
    MatchNotFoundError is raised unless a default value is given, In which case the default value is returned.

    @param expression: The path expression that define the search criteria.
    @param data: The data to search through.  The data must be either a tree structure that adheres to
        https://docs.python.org/3/library/json.html or a Match object from a previous search.
    @param default:  An optional value to return when no result is found.
    @param trace: An optional callable to report detail iteration data too.
    @return: The value that satisfies the path expression, else MatchNotFoundError is raised unless default is given.
    @raise MatchNotFoundError:  Raised when no result is found and no default value is given.
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
    Construct a lazy iterator of all values in the data that satisfies the path expression.

    @param expression: The path expression that define the search criteria.
    @param data: The data to search through.  The data must be either a tree structure that adheres to
        https://docs.python.org/3/library/json.html or a Match object from a previous search.
    @param trace: An optional callable to report detail iteration data too.
    @return: A lazy iterator containing all values that satisfies the path expression.
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
    Returns the first Match in the data that satisfies the path expression.   When no result is found, a
    MatchNotFoundError is raised unless must_match is False, In which case None is returned.

    @param expression: The path expression that define the search criteria.
    @param data: The data to search through.  The data must be either a tree structure that adheres to
        https://docs.python.org/3/library/json.html or a Match object from a previous search.
    @param must_match:  An optional argument to indicate whether to raise MatchNotFoundError or return None when no
        result is found. By default MatchNotFoundError will be raise.
    @param trace: An optional callable to report detail iteration data too.
    @return: The Match that satisfies the path expression, else MatchNotFoundError is raised unless default is given.
    @raise MatchNotFoundError:  Raised when no result is found and must_match is set to True.
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
    Construct a lazy iterator of all Matches in the data that satisfies the path expression.

    @param expression: The path expression that define the search criteria.
    @param data: The data to search through.  The data must be either a tree structure that adheres to
        https://docs.python.org/3/library/json.html or a Match object from a previous search.
    @param trace: An optional callable to report detail iteration data too.
    @return: A lazy iterator containing all Matches that satisfies the path expression.
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
    Construct a lazy iterator of all values in the parent Match that satisfies the path expression. As a convenience,
    the find function also accepts the Match object as source data, so it not necessary to use this function directly.

    @param expression: The path expression that define the search criteria.
    @param parent_match: The data to search through.  The data must be a Match object from a previous search.
    @param trace: An optional callable to report detail iteration data too.
    @return: A lazy iterator containing all values that satisfies the path expression.
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
    Returns the first Match in the parent Match that satisfies the path expression.   When no result is found, a
    MatchNotFoundError is raised unless must_match is False, In which case None is returned.  As a convenience, the
    get_match function also accepts the Match object as source data, so it not necessary to use this function directly.

    @param expression: The path expression that define the search criteria.
    @param parent_match: The data to search through.  The data must be a Match object from a previous search.
    @param must_match:  An optional argument to indicate whether to raise MatchNotFoundError or return None when no
        result is found. By default MatchNotFoundError will be raise.
    @param trace: An optional callable to report detail iteration data too.
    @return: The Match that satisfies the path expression, else MatchNotFoundError is raised unless default is given.
    @raise MatchNotFoundError:  Raised when no result is found and must_match is set to True.
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
    Construct a lazy iterator of all Matches in the parent Match that satisfies the path expression.  As a convenience,
    the find_matches function also accepts the Match object as source data, so it not necessary to use this function
    directly.

    @param expression: The path expression that define the search criteria.
    @param parent_match: The data to search through.  The data must be a Match object from a previous search.
    @param trace: An optional callable to report detail iteration data too.
    @return: A lazy iterator containing all Matches that satisfies the path expression.
    """
    if isinstance(parent_match, PredicateMatch):
        trace = parent_match.trace
    vertex = get_vertex_from_path_builder(expression)
    traverser = NestedMatchTraverser(parent_match._traverser_match, vertex, trace=trace)
    traverser_iter = iter(traverser)
    return traverser_iter


def has_these(*args: _has_multiple_arg_type, repr_join_key=', '):
    """
    The has these decorator defines an aggregates predicate.   It augments the path predicate its decorating with the
    decorator arguments.

    For example:
    #          arg1     arg2       arg3                      arg4
    @has.these(path.a,  path.b==2, (path.c, operator.truth), other_predicate)
    def predicate(match: Match, arg1, arg2, arg3, arg4):
     return return arg1(match) and arg2(match) and arg3(match) and arg4(match)
    value = get(path.rec[predicate].name,solar_system)

    @param args: Varying number of positional arguments.  Each argument must be a path expression or a path predicate.
    @param repr_join_key:  A string to use as a delimiter when joining the arguments while pretty printing path.
    @return: The decorated function to be used as a path predicate in a path expression.
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


def has_all(*args: _has_multiple_arg_type) -> Callable[[Match], Any]:
    """
    Construct a logical and predicate.   The outcome of evaluating the predicate is equivalent to
    return arg0(match) and arg1(match) and arg2(match) ... and argN(match)

    Example Usage
    * get(path.a[has_all(path.b, path.z)].c) interpret as get a.c if both a.b and a.z exist.
    * get(path.a[has_all(path.b, path.z==1)].c) interpret as get a.c if a.b exist and a.z==1.
    * get(path.a[has_all(path.b, (path.z==1, int))].c) interpret as get a.c if a.b exist and int(a.z)==1.
    * get(path.a[has_all(path.b, has(path.z==1, int))].c) has same meaning as previous.
    * get(path.a[has_all(has_any(path.l,path.m),has_any(path.x,path.y))].c) interpret as get a.c if either a.l or a.m
      exist and if either a.x or a.y exist.

    @param args: A variable length argument where each argument may be a path expression,  a path expression with
           condition operator, a predicate or a tuple.  A tuple argument is interpreted as a has function.
    @return:  Returns a predicate that performs a logical and on the arguments.
    """

    @has.these(*args, repr_join_key=' and ')
    def and_predicate(parent_match: Match, *predicates) -> Any:
        for predicate in predicates:
            if not predicate(parent_match):
                return False
        return True

    return and_predicate


def has_any(*args: _has_multiple_arg_type) -> Callable[[Match], Any]:
    """
    Construct a logical or predicate.   The outcome of evaluating the predicate is equivalent to
    return arg0(match) or arg1(match) or arg2(match) ... or argN(match)

    Example Usage
    * get(path.a[has_any(path.b, path.z)].c) interpret as get a.c if either a.b or a.z exist.
    * get(path.a[has_any(path.b, path.z==1)].c) interpret as get a.c if either a.b exist or a.z==1.
    * get(path.a[has_any(path.b, (path.z==1, int))].c) interpret as get a.c if either a.b exist or int(a.z)==1.
    * get(path.a[has_any(path.b, has(path.z==1, int))].c) has same meaning as previous.
    * get(path.a[has_any(has_all(path.l,path.m),has_all(path.x,path.y))].c) interpret as get a.c if a.l and a.m
      exist or if a.x and a.y exist.

    @param args: A variable length argument where each argument may be a path expression,  a path expression with
           condition operator, a predicate or a tuple.  A tuple argument is interpreted as a has function.
    @return:  Returns a predicate that performs a logical or on the arguments.
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
    Construct a logical not predicate.  The has_not functions accepts the same
    arguments as the has function.

    Example Usage
     * get(path.a[has_not(path.b)].c) interpret as get a.c if  a.b does not exist.
     * get(path.a[has_not(has(path.b))].c) has same meaning as previous.
     * get(path.a[has_not(has_any(path.b, path.z))].c) interpret as get a.c if both a.b and a.z do not exist.


    @param path: A path expression,  a path expression with condition operator, or predicate.
    @param single_arg_functions:  A variable argument of or Callable[[ANY],ANY].   The Callables are evaluated as
           follows: arg0(arg1(arg2(...argN(get(path)))).

    @return:  Returns the constructed not predicate.
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
    Constructs a predicate from a path expression, a path expression and condition, a path expression, a
    condition and a map function or a predicate.  These four forms are shown here:

    First form: has(path expression)
    * Evaluates true if the path expression combined with parent path expression exist.
    * get(path.a[has(path.b)].c) interpret as get a.c if a.b exist.

    Second form: has(path expression, condition)
    * Applies the condition to the value referenced by the path expression combined with parent path expression.
    * The condition can be either a single argument function that returns a value or any of the following operators:
      ==, !=, >, >=, <, or <=.
    * get(path.a[has(path.b, operator.truth)].c) interpret as get a.c if operator.truth(get(a.b)).
    * get(path.a[has(path.b==1)].c) interpret as get a.c if get(a.b)==1.

    Third form: has(path expression, condition, map function)
    * First applies the map function to the value referenced by the path expression combined with parent path
      expression. Next apply the condition to the value return from map function.
    * The map function must be a single argument function that returns a value.
    * get(path.a[has(path.b,  operator.truth, int)].c) interpret as get a.c if operator.truth(int(get(a.b))).
    * get(path.a[has(path.b==1, int)].c) interpret as get a.c if int(get(a.b))==1.

    Fourth form: has(path predicate)
    * Return the path predicate argument.
    * A path predicate type:  Callable[[Match], ANY]
    * get(path.a[has(has(path.b))].c) == get(path.a[has(path.b)].c)

    @param path: A path expression,  a path expression with condition operator, or predicate.
    @param single_arg_functions:  A variable argument of or Callable[[ANY],ANY].   The Callables are evaluated as
           follows: arg0(arg1(arg2(...argN(get(path)))).

    @return:  Returns the constructed predicate.
    """
    return create_has_predicate(nested_find_matches, path, *single_arg_functions)

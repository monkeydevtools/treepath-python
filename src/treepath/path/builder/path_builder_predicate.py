import operator

from treepath.path.builder.path_predicate import PathPredicate
from treepath.path.util.decorator import pretty_repr
from treepath.path.util.function import create_partial_operator


class PathBuilderPredicate:
    __slots__ = ()

    def __lt__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__lt__, other)
        pretty = pretty_repr(lambda: f"< {other}")
        return PathPredicate(self, pretty(operator_))

    def __le__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__le__, other)
        pretty = pretty_repr(lambda: f"<= {other}")
        return PathPredicate(self, pretty(operator_))

    def __eq__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__eq__, other)
        pretty = pretty_repr(lambda: f"== {other}")
        return PathPredicate(self, pretty(operator_))

    def __ne__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__ne__, other)
        pretty = pretty_repr(lambda: f"!= {other}")
        return PathPredicate(self, pretty(operator_))

    def __gt__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__gt__, other)
        pretty = pretty_repr(lambda: f"> {other}")
        return PathPredicate(self, pretty(operator_))

    def __ge__(self, other) -> PathPredicate:
        operator_ = create_partial_operator(operator.__ge__, other)
        pretty = pretty_repr(lambda: f">= {other}")
        return PathPredicate(self, pretty(operator_))

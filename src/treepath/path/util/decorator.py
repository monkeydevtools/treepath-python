from typing import Callable


def pretty_repr(pretty_rep_: Callable[[], str]):
    class PrettyRep:
        __slots__ = '_operator', '_pretty_rep'

        def __init__(self, operator_):
            self._operator = operator_
            self._pretty_rep = pretty_rep_

        def __call__(self, *args):
            return self._operator(*args)

        def __repr__(self):
            return self._pretty_rep()

        def __str__(self):
            return self._pretty_rep()

    return PrettyRep


def add_attr(attr_name, attr_value):
    def _add_attr(func):
        setattr(func, attr_name, attr_value)
        return func

    return _add_attr

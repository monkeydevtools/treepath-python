from typing import Callable


def do_nothing(value):
    """
    Return the argument
    return the argument value
    """
    return value


def pretty_rep(pretty_rep_: Callable[[], str]):
    class PrettyRep:
        __slots__ = '_operator', '_pretty_rep'

        def __init__(self, operator_):
            self._operator = operator_
            self._pretty_rep = pretty_rep_

        def __call__(self, arg):
            return self._operator(arg)

        def __repr__(self):
            return self._pretty_rep()

    return PrettyRep

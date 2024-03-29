from typing import Callable, Union

from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class Trace:
    """
    The Trace class contains the details that describes the context of the intermediate state of the traversal
    algorithm.  When tracing a path, an instance of this class is passed as an argument to the tracing Callable on each
    match is attempted.

    The three properties last_match, next_vertex and next_match form the following function.
    next_match = next_vertex.match(last_match)

    """
    __slots__ = '_last_match', '_next_match', '_next_vertex', '_predicate_match'

    def __init__(self, last_match: Match, next_match: Match, next_vertex: Vertex):
        self._last_match = last_match
        self._next_match = next_match
        self._next_vertex = next_vertex
        self._predicate_match = None

    @property
    def last_match(self) -> Match:
        """
        Return the Match used as input to  self.next_vertex
        """
        return self._last_match

    @property
    def next_match(self) -> Union[Match, None]:
        """
        Return the next successful Match generated by self.next_vertex.  None is returned  if none Match was found.
        """
        return self._next_match

    @property
    def next_vertex(self) -> Vertex:
        """
        Return the current matching algorithm being applied.
        """
        return self._next_vertex

    @property
    def predicate_match(self) -> Union[Match, None]:
        """
        Returns the parent match to the predicate.  This Match indicates the traversal algorithm is currently traversing
        the predicate part of a path.   None is return when this is not occurring.
        """
        return self._predicate_match

    @predicate_match.setter
    def predicate_match(self, predicate_match: Match):
        if not self._predicate_match:
            self._predicate_match = predicate_match


def _log(log: Callable[[str], None], trace: Trace):
    last_path = trace.last_match.path_as_str
    vertex_path_segment = trace.next_vertex.path_segment
    if trace.next_match:
        data = repr(trace.next_match.data)
        trunc_data = data if len(data) < 20 else data[:20] + '...'
        result = f"{trunc_data}"
    else:
        result = 'no match'
    message = f" at {last_path}{vertex_path_segment} got {result}"

    if trace.predicate_match:
        predicate_path = f" at {trace.predicate_match.path_as_str}"
        message = message.replace(predicate_path, " has ".rjust(len(predicate_path)), 1)

    log(message)


def log_to(out: Callable[[str], None]):
    """
    Returns tracer Callable that passes str representation of the Trace Class to the out Callable. Examples:
    log_to(print) log_to(logger.debug)

    :param out: A callable to invoke with the str representation of Trace Class
    :returns:  A  Callable[[Trace], None]
    """
    def to_out(trace: Trace):
        _log(out, trace)

    return to_out

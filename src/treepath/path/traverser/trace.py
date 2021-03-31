import logging
from typing import Callable

from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class Trace:
    __slots__ = '_last_match', '_next_match', '_next_vertex', '_predicate_match'

    def __init__(self, last_match: Match, next_match: Match, next_vertex: Vertex):
        self._last_match = last_match
        self._next_match = next_match
        self._next_vertex = next_vertex
        self._predicate_match = None

    @property
    def last_match(self) -> Match:
        return self._last_match

    @property
    def next_match(self) -> Match:
        return self._next_match

    @property
    def next_vertex(self) -> Vertex:
        return self._next_vertex

    @property
    def predicate_match(self) -> Match:
        return self._predicate_match

    @predicate_match.setter
    def predicate_match(self, predicate_match: Match):
        if not self._predicate_match:
            self._predicate_match = predicate_match


def _log(log: Callable[[str], None], trace: Trace):
    last_path = trace.last_match.path
    vertex_path_segment = trace.next_vertex.path_segment
    if trace.next_match:
        next_match_path_segment = trace.next_match.path_segment
        data = repr(trace.next_match.data)
        trunc_data = data if len(data) < 20 else data[:20] + '...'
        result = f"{next_match_path_segment} == {trunc_data}"
    else:
        result = 'no match'
    message = f" at {last_path}{vertex_path_segment} got {result}"

    if trace.predicate_match:
        predicate_path = f" at {trace.predicate_match.path}"
        message = message.replace(predicate_path, " has ".rjust(len(predicate_path)), 1)

    log(message)


def log_to(out: Callable[[str], None]):
    def to_out(trace: Trace):
        _log(out, trace)

    return to_out



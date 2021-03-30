import logging
from typing import Callable

from treepath import Match
from treepath.path.vertex.vertex import Vertex


def trace(last_match: Match, next_match: Match, next_vertex: Vertex, predicate_match: Match = None):
    pass


def _log(log: Callable[[str], None], last_match: Match, next_match: Match, next_vertex: Vertex,
         predicate_match: Match = None):
    last_path = last_match.path
    vertex_path_segment = next_vertex.path_segment
    if next_match:
        next_match_path_segment = next_match.path_segment
        data = repr(next_match.data)
        trunc_data = data if len(data) < 20 else data[:20] + '...'
        result = f"{next_match_path_segment} == {trunc_data}"
    else:
        result = 'no match'
    message = f" at {last_path}{vertex_path_segment} got {result}"

    if predicate_match:
        predicate_path = f" at {predicate_match.path}"
        message = message.replace(predicate_path, " has".ljust(len(predicate_path)), 1)


    log(message)


def to(out: Callable[[str], None]):
    def to_out(last_match, next_match, next_vertex, predicate_match: Match = None):
        _log(out, last_match, next_match, next_vertex, predicate_match=predicate_match)

    return to_out


def to_logger(last_match: Match, next_match: Match, next_vertex: Vertex, predicate_match: Match = None):
    return _log(logging.getLogger("treepath").info, last_match, next_match, next_vertex,
                predicate_match=predicate_match)


def to_console(last_match: Match, next_match: Match, next_vertex: Vertex, predicate_match: Match = None):
    return _log(print, last_match, next_match, next_vertex, predicate_match=predicate_match)

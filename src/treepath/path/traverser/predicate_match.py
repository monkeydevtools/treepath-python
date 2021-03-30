from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class PredicateMatch(Match):
    __slots__ = '_trace'

    def __init__(self, trace, *args):
        super().__init__(*args)
        self._trace = trace

    @property
    def trace(self):

        trace = self._trace

        if trace:
            def predicate_trace(last_match: Match, next_match: Match, next_vertex: Vertex,
                                predicate_match: Match = None):
                if predicate_match:
                    trace(last_match, next_match, next_vertex, predicate_match=predicate_match)
                else:
                    trace(last_match, next_match, next_vertex, predicate_match=self)

            return predicate_trace
        else:
            return None

from treepath.path.traverser.match import Match
from treepath.path.traverser.trace import Trace


class PredicateMatch(Match):
    __slots__ = '_trace'

    def __init__(self, trace, *args):
        super().__init__(*args)
        self._trace = trace

    @property
    def trace(self):
        trace_function = self._trace
        if trace_function:
            def predicate_trace(trace: Trace):
                trace.predicate_match = self
                trace_function(trace)

            return predicate_trace
        else:
            return None

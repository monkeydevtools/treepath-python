from typing import Callable

from treepath.path.traverser.match import Match
from treepath.path.traverser.imaginary_match import ImaginaryMatch
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.trace import Trace
from treepath.path.vertex.vertex import Vertex


class NestedMatchTraverser(MatchTraverser):
    __slots__ = 'nested_match'

    def __init__(self,
                 nested_match: Match,
                 leaf_vertex: Vertex,
                 trace: Callable[[Trace], None] = None
                 ):
        traverser_match = nested_match._traverser_match
        super().__init__(traverser_match.data, leaf_vertex, trace=trace)
        self.nested_match = traverser_match

    def init_action(self):
        vertex = self.vertex_path[0]
        root_match = ImaginaryMatch(
            self.nested_match,  # real_parent
            vertex.name,
            self.root_data,  # data
            vertex,
            0,  # vertex_index,
            None,  # remembered_on_catch_match
            self.done_action
        )
        root_match.remembered_on_catch_match = root_match
        self.root_match = root_match
        self.current_match = root_match
        self._invoke_next_action = self.report_action

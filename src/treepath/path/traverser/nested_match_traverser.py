from treepath.path.traverser.imaginary_match import ImaginaryMatch
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class NestedMatchTraverser(MatchTraverser):
    __slots__ = 'nested_match'

    def __init__(self, nested_match: TraverserMatch, leaf_vertex: Vertex):
        super().__init__(nested_match.data, leaf_vertex)
        self.nested_match = nested_match

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

from treepath.path.traverser.empty_match import EmptyMatch
from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.vertex.vertex import Vertex


class NestedMatchTraverser(MatchTraverser):

    def __init__(self, nested_match: Match, leaf_vertex: Vertex):
        super().__init__(nested_match.data, leaf_vertex)
        self.nested_match = nested_match

    def init_action(self):
        vertex = self.vertex_path[0]
        root_match = EmptyMatch(
            self.nested_match,  # parent
            vertex.name,
            self.root_data,  # data
            vertex,  # vertex
            None,  # remembered_on_catch_match
            self.done_action
        )
        root_match.vertex_index = 0
        root_match.remembered_on_catch_match = root_match
        self.current_match = root_match
        self._invoke_next_action = self.match_action

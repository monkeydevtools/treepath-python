from treepath.path.exceptions.stop_traversing import StopTraversing
from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.match import Match
from treepath.path.traverser.root_match import RootMatch
from treepath.path.vertex.vertex import Vertex


class MatchTraverser:

    def __init__(self, root_data, leaf_vertex: Vertex):
        self.vertex_path = leaf_vertex.path_as_list
        self.leaf_vertex = leaf_vertex
        self.root_data = root_data
        self._invoke_next_action = self.done_action
        self.current_match = None
        self.root_match = None

    def __iter__(self):
        self._invoke_next_action = self.init_action
        return self

    def __next__(self) -> Match:
        result = None
        while not result:
            result = self._invoke_next_action()
        return self.current_match

    def remember_on_catch(self, match, remembered_catch_state):
        match.remembered_catch_state = remembered_catch_state
        match.remembered_on_catch_match = match
        match.remembered_on_catch_action = self.match_action

    def restore_on_catch(self, match):
        match.remembered_catch_state = None
        if self.root_match == match:
            match.remembered_on_catch_match = None
            match.remembered_on_catch_action = self.done_action()
        else:
            parent = match.parent
            match.remembered_on_catch_match = parent.remembered_on_catch_match
            match.remembered_on_catch_action = parent.remembered_on_catch_action

    def init_action(self):
        vertex = self.vertex_path[0]
        root_match = RootMatch(
            None,  # parent
            vertex.name,
            self.root_data,  # data
            vertex,  # vertex
            None,  # remembered_on_catch_match
            self.done_action
        )
        root_match.vertex_index = 0
        root_match.remembered_on_catch_match = root_match
        self.root_match = root_match
        self.current_match = root_match
        self._invoke_next_action = self.match_action

        if not self.leaf_vertex.parent:
            raise TraversingError(
                root_match,
                "Invalid path.   The root vertex in the path must have at least one child path vertex.  "
            )

    def match_action(self):
        current_match = self.current_match
        next_vertex_index = current_match.vertex_index
        next_vertex_index += 1
        next_vertex = self.vertex_path[next_vertex_index]

        # apply the match
        next_match = next_vertex.match(current_match, self)

        if next_match:
            next_match.vertex_index = next_vertex_index
            self.current_match = next_match
            self._invoke_next_action = self.report_action
        else:
            self.current_match = current_match.remembered_on_catch_match
            self._invoke_next_action = current_match.remembered_on_catch_action

    def recursive_match_action(self):
        current_match = self.current_match
        current_match.remembered_on_catch_action = self.match_action

        next_vertex_index = current_match.vertex_index
        next_vertex_index += 1
        next_vertex = self.vertex_path[next_vertex_index]

        # apply the match
        next_match = next_vertex.recursive_match(current_match)

        if next_match:
            next_match.vertex_index = next_vertex_index - 1
            self.current_match = next_match
            self._invoke_next_action = self.match_action
        else:
            self.current_match = current_match.remembered_on_catch_match
            self._invoke_next_action = current_match.remembered_on_catch_action

    def post_recursive_match_action(self):
        pass

    def report_action(self):
        current_match = self.current_match
        if current_match.vertex == self.leaf_vertex:
            self._invoke_next_action = self.catch_action
            return True
        else:
            self._invoke_next_action = self.match_action

    def catch_action(self):
        current_match = self.current_match
        self.current_match = current_match.remembered_on_catch_match
        self._invoke_next_action = current_match.remembered_on_catch_action

    def done_action(self):
        raise StopTraversing(self.leaf_vertex)

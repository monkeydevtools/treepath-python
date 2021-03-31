from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class NestedMatchNotFoundError(MatchNotFoundError, LookupError):
    """
    MatchNotFoundError is raised when a get_match is expected; however, the data structure has no more element to traverse
    """

    def __init__(self, nested_match: Match, vertex: Vertex):
        super().__init__(vertex)
        self.nested_match = nested_match

    def _resolve_msg(self):
        path = repr(self.vertex)
        nested_path = self.nested_match.path
        return f"No get_match occurred on path: {nested_path}({path})"

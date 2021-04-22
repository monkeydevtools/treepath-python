from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class NestedMatchNotFoundError(MatchNotFoundError, LookupError):
    """
    NestedMatchNotFoundError is raised when nested_get_match query fails to generate a result for the specified path.
    """

    def __init__(self, nested_match: Match, vertex: Vertex):
        super().__init__(vertex)
        self.nested_match = nested_match

    def _resolve_msg(self):
        path = repr(self.vertex)
        nested_path = self.nested_match.path
        return f"NestedMatchNotFoundError(No get_match occurred on path {path} from match {nested_path})"

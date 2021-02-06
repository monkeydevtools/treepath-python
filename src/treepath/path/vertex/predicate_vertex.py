from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.empty_match import EmptyMatch
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class PredicateVertex(Vertex):
    def __init__(self, parent, predicate):
        self._predicate = predicate
        super().__init__(parent, predicate)

    def path_segment(self):
        return f"[{self._predicate}]"

    def match(self, parent_match: Match, traverser) -> object:

        try:
            if self._predicate(parent_match):
                match = EmptyMatch(
                    parent_match,
                    "PredicateMatch",
                    parent_match.data,
                    self,
                    parent_match.remembered_on_catch_match,
                    parent_match.remembered_on_catch_action
                )
                return match
        except TraversingError as te:
            raise te
        except Exception as e:
            error_message = f"Evaluation of predicate failed because of error: {e}"
            raise TraversingError(parent_match, error_message) from e

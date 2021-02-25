from typing import Union

from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.imaginary_match import ImaginaryMatch
from treepath.path.traverser.match import Match
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class PredicateVertex(Vertex):
    __slots__ = '_predicate'

    def __init__(self, parent, predicate):
        self._predicate = predicate
        super().__init__(parent, predicate)

    def path_segment(self):
        return f"[{self._predicate}]"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        try:
            if self._predicate(Match(parent_match)):
                match = ImaginaryMatch(
                    parent_match,
                    "PredicateMatch",
                    parent_match.data,
                    self,
                    vertex_index,
                    parent_match.remembered_on_catch_match,
                    parent_match.remembered_on_catch_action
                )
                return match
        except TraversingError as te:
            raise te
        except Exception as e:
            error_message = f"Evaluation of predicate failed because of error: {e}"
            raise TraversingError(parent_match, error_message) from e

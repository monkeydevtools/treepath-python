from typing import Union

from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.imaginary_match import ImaginaryMatch
from treepath.path.traverser.match import Match
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.list_vertex import ListWildVertex
from treepath.path.vertex.vertex import Vertex


class PredicateListWildVertex(ListWildVertex):
    pass


class PredicateVertex(Vertex):
    __slots__ = '_predicate', \
                '_predicate_list_wild_vertex'

    def __init__(self, parent, predicate):
        self._predicate = predicate
        self._predicate_list_wild_vertex = PredicateListWildVertex(parent)
        super().__init__(parent, predicate)

    def path_segment(self):
        return f"[{self._predicate}]"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        #  This code eliminates the wc before the has [wc][has(path.name)]
        # if not isinstance(parent_match.vertex, PredicateListWildVertex) and isinstance(parent_match.data, list):
        #     lwv = ListWildVertex(parent_match.vertex)
        #     return lwv.match(parent_match, traverser, vertex_index - 1)

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

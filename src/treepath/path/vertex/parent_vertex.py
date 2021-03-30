from typing import Union

from treepath.path.traverser.parent_match import ParentMatch
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class ParentVertex(Vertex):
    __slots__ = ()

    def __init__(self, parent):
        super().__init__(parent, "parent")

    @property
    def path_segment(self):
        return f".{self.name}"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:
        remembered_parent = parent_match.remembered_parent

        if not remembered_parent:
            return None

        return ParentMatch(
            remembered_parent,
            parent_match,
            remembered_parent.data_name,
            remembered_parent.data,
            self,
            vertex_index,
            parent_match.remembered_on_catch_match,
            parent_match.remembered_on_catch_action
        )

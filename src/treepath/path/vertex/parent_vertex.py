from typing import Union

from treepath.path.traverser.key_match import KeyMatch
from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class ParentVertex(Vertex):
    __slots__ = ()

    def __init__(self, parent):
        super().__init__(parent, "parent")

    def path_segment(self):
        return f".{self.name}"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        grand_parent = parent_match.parent

        if not grand_parent:
            return None

        grand_parent_data = grand_parent.data

        if isinstance(grand_parent_data, dict):
            constructor = KeyMatch
        elif isinstance(grand_parent_data, list):
            constructor = ListMatch
        else:
            return None

        return constructor(
            parent_match,
            f"<-{grand_parent.data_name}",
            grand_parent_data,
            self,
            vertex_index,
            parent_match.remembered_on_catch_match,
            parent_match.remembered_on_catch_action
        )

import typing

from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class RootVertex(Vertex):
    __slots__ = ()

    def __init__(self, name: str):
        super().__init__(None, name)
        self._path_as_list = [self]

    @property
    def path_as_list(self) -> list:
        return self._path_as_list

    @property
    def path(self) -> str:
        return self.name

    def traverse(self, visit: typing.Callable[[Vertex], None]):
        visit(self)

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> typing.Union[TraverserMatch, None]:
        raise TraversingError(parent_match, f"Possible Bug.  The root match method should never be called.")

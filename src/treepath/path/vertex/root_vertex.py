import typing

from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class RootVertex(Vertex):
    def __init__(self, name: str):
        super().__init__(None, name)
        self._path_as_list = [self]

    @property
    def path_as_list(self) -> list:
        return self._path_as_list

    @property
    def path(self):
        return self.name

    def traverse(self, visit: typing.Callable):
        visit(self)

    def match(self, parent_match: Match, traverser) -> object:
        raise TraversingError(parent_match, f"The path {self.name} is not traversable.  ")

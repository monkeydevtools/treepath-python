import functools
import typing
from abc import ABC

from treepath.path.traverser.match import Match


class Vertex(ABC):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.is_catch_vertex = False

    @functools.cached_property
    def path_as_list(self) -> list:
        vertex_list = []

        def collect(vertex):
            vertex_list.append(vertex)

        self.traverse(collect)
        return vertex_list

    @functools.cached_property
    def path(self):
        return ''.join(vertex.path_segment() for vertex in self.path_as_list)

    def path_segment(self):
        return self.name

    def traverse(self, visit: typing.Callable):
        self.parent.traverse(visit)
        visit(self)

    def match(self, parent_match: Match, traverser) -> Match:
        raise NotImplementedError

    def __repr__(self):
        return self.path

    def __str__(self):
        return self.__repr__()

from typing import Union, Callable

from treepath.path.traverser.traverser_match import TraverserMatch


class Vertex:
    __slots__ = 'parent', \
                'name', \
                'is_catch_vertex', \
                '_path_as_list', \
                '_path'

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.is_catch_vertex = False
        self._path_as_list = self
        self._path = self

    @property
    def path_as_list(self) -> list:
        path_as_list = self._path_as_list
        if path_as_list != self:
            return path_as_list

        path_as_list = []

        def collect(vertex):
            path_as_list.append(vertex)

        self.traverse(collect)

        self._path_as_list = path_as_list

        return path_as_list

    @property
    def path(self):
        path = self._path
        if path != self:
            return path

        path_as_list = self.path_as_list
        path = ''.join(vertex.path_segment() for vertex in path_as_list)
        self._path = path
        return path

    def path_segment(self):
        return self.name

    def traverse(self, visit: Callable):
        self.parent.traverse(visit)
        visit(self)

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:
        raise NotImplementedError

    def __repr__(self):
        return self.path

    def __str__(self):
        return self.__repr__()

import functools
import typing
from abc import ABC


class Match(ABC):

    def __init__(self,
                 parent,
                 data_name,
                 data,
                 vertex,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        self.parent = parent
        self.data_name = data_name
        self.data = data
        self.vertex = vertex
        self.vertex_index = 0
        self.remembered_catch_state = None
        self.remembered_on_catch_match = remembered_on_catch_match
        self.remembered_on_catch_action = remembered_on_catch_action

    @functools.cached_property
    def path_as_list(self) -> list:
        match_list = []

        def collect(vertex):
            match_list.append(vertex)

        self.traverse(collect)
        return match_list

    @functools.cached_property
    def path(self):
        return ''.join(match.path_segment() for match in self.path_as_list)

    def path_segment(self):
        raise NotImplementedError

    def traverse(self, visit: typing.Callable):
        self.parent.traverse(visit)
        visit(self)

    def __repr__(self):
        return f"{self.path}={self.data}"

    def __str__(self):
        return self.__repr__()

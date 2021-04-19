from abc import abstractmethod, ABC, abstractproperty
from typing import List, Any, Callable


class TraverserMatch(ABC):
    __slots__ = 'real_parent', \
                'real_data_name', \
                'data', \
                'vertex', \
                'vertex_index', \
                '_path_as_list', \
                '_path', \
                'remembered_catch_state', \
                'remembered_on_catch_match', \
                'remembered_on_catch_action'

    def __init__(self,
                 real_parent,
                 data_name,
                 data,
                 vertex,
                 vertex_index,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        self.real_parent = real_parent
        self.real_data_name = data_name
        self.data = data
        self.vertex = vertex
        self.vertex_index = vertex_index
        self._path_as_list = self
        self._path = self
        self.remembered_catch_state = None
        self.remembered_on_catch_match = remembered_on_catch_match
        self.remembered_on_catch_action = remembered_on_catch_action

    @property
    def path_as_list(self) -> List[Any]:
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
    def path(self) -> str:
        path = self._path
        if path != self:
            return path

        path_as_list = self.path_as_list
        path = ''.join(match.path_segment for match in path_as_list)
        self._path = path
        return path

    @property
    @abstractmethod
    def path_segment(self) -> str:
        raise NotImplementedError

    @property
    def data_name(self) -> str:
        return self.real_data_name

    @property
    def parent(self):
        return self.real_parent

    @property
    def remembered_parent(self):
        return self.parent

    def traverse(self, visit: Callable[[Any], None]):
        self.real_parent.traverse(visit)
        visit(self)

    def __repr__(self):
        return f"{self.path}={self.data}"

    def __str__(self):
        real_parent = id(self.real_parent)
        data_name = self.real_data_name
        data = type(self.data).__name__
        vertex = type(self.vertex).__name__
        vertex_index = self.vertex_index
        remembered_catch_state = type(self.remembered_catch_state).__name__
        remembered_on_catch_match = id(self.remembered_on_catch_match)
        remembered_on_catch_action = type(self.remembered_on_catch_action).__name__
        path = self.path

        return f"self={id(self)}" \
               f" self={type(self).__name__}" \
               f" parent={real_parent}" \
               f" real_data_name={data_name}" \
               f" data={data}" \
               f" vertex={vertex}" \
               f" vertex_index={vertex_index}" \
               f" remembered_catch_state={remembered_catch_state}" \
               f" remembered_on_catch_match={remembered_on_catch_match}" \
               f" remembered_on_catch_action={remembered_on_catch_action}" \
               f" path={path}"

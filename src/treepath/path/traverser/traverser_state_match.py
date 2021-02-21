import typing


class TraverserStateMatch:
    __slots__ = 'real_parent', \
                'data_name', \
                'data', \
                'vertex', \
                '_path_as_list', \
                '_path', \
                'vertex_index', \
                'remembered_catch_state', \
                'remembered_on_catch_match', \
                'remembered_on_catch_action'

    def __init__(self,
                 real_parent,
                 data_name,
                 data, vertex,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        self.real_parent = real_parent
        self.data_name = data_name
        self.data = data
        self.vertex = vertex
        self._path_as_list = self
        self.remembered_catch_state = None
        self.remembered_on_catch_match = remembered_on_catch_match
        self.remembered_on_catch_action = remembered_on_catch_action
        self._path = self
        self.vertex_index = 0

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
        path = ''.join(match.path_segment for match in path_as_list)
        self._path = path
        return path

    @property
    def path_segment(self):
        raise NotImplementedError

    @property
    def parent(self):
        raise self.real_parent



    def traverse(self, visit: typing.Callable):
        self.real_parent.traverse(visit)
        visit(self)

    def __repr__(self):
        return f"{self.path}={self.data}"

    def __str__(self):
        return self.__repr__()

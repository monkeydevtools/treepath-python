import typing


class Match:
    __slots__ = '_parent', \
                '_data_name', \
                'data', \
                '_vertex', \
                '_path_as_list', \
                '_path'

    def __init__(self,
                 parent,
                 data_name,
                 data,
                 vertex,
                 ):
        self._parent = parent
        self._data_name = data_name
        self.data = data
        self._vertex = vertex
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
        path = ''.join(match.path_segment for match in path_as_list)
        self._path = path
        return path

    @property
    def path_segment(self):
        raise NotImplementedError

    @property
    def parent(self):
        return self._parent

    @property
    def data_name(self):
        return self._data_name

    @property
    def vertex(self):
        return self._vertex

    def traverse(self, visit: typing.Callable):
        self._parent.traverse(visit)
        visit(self)

    def __repr__(self):
        return f"{self.path}={self.data}"

    def __str__(self):
        return self.__repr__()

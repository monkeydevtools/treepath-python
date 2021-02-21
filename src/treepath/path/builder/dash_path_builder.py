from treepath.path.builder.path_builder import _RESERVED_ATTR_FOR_VERTEX_DATA, PathBuilder
from treepath.path.vertex.key_vertex import KeyVertex
from treepath.path.vertex.root_vertex import RootVertex


class DashPathBuilder(PathBuilder):
    __slots__ = ()

    def __init__(self, vertex):
        super().__init__(vertex)

    def __getattr__(self, name: str):
        """
        creates a new attribute at self.
        This method only get called if self.name does not already exist
        self.name
        """
        name = name.replace('_', '-')
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = KeyVertex(parent_vertex, name)
        path_builder = DashPathBuilder(vertex)
        return path_builder


class DashPathRoot(DashPathBuilder):
    __slots__ = ()

    def __init__(self):
        vertex = RootVertex("$")
        super().__init__(vertex)

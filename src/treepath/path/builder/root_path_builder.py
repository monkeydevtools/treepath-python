from treepath.path.builder.path_builder import PathBuilder
from treepath.path.vertex.root_vertex import RootVertex


class RootPathBuilder(PathBuilder):
    __slots__ = ()

    def __init__(self):
        vertex = RootVertex("$")
        super().__init__(vertex)

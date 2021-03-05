from treepath.path.builder.path_builder import PathBuilder
from treepath.path.vertex.root_vertex import RootVertex


class DashPathBuilder(PathBuilder):
    __slots__ = ()

    def create_path_builder(self, *args, **kwargs):
        return DashPathBuilder(*args, **kwargs)

    def tranform_attribute_name(self, name):
        return name.replace('_', '-')


class DashPathRoot(DashPathBuilder):
    __slots__ = ()

    def __init__(self):
        vertex = RootVertex("$")
        super().__init__(vertex)

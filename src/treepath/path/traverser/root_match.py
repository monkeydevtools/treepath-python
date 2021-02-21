import typing

from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class RootMatch(TraverserStateMatch):
    __slots__ = ()

    def __init__(self,
                 parent,
                 data_name, data,
                 vertex,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        TraverserStateMatch.__init__(self,
                                     parent,
                                     data_name,
                                     data,
                                     vertex,
                                     remembered_on_catch_match,
                                     remembered_on_catch_action
                                     )
        self._path_as_list = [self]

    @property
    def path_as_list(self) -> list:
        return self._path_as_list

    @property
    def path(self):
        return self.data_name

    @property
    def path_segment(self):
        return self.data_name

    def traverse(self, visit: typing.Callable):
        visit(self)

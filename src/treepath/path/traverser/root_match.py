import typing

from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class RootMatch(TraverserStateMatch):
    __slots__ = ()

    @property
    def path_as_list(self) -> list:
        return [self]

    @property
    def path(self):
        return self.data_name

    @property
    def path_segment(self):
        return self.data_name

    def traverse(self, visit: typing.Callable):
        visit(self)

import typing

from treepath.path.traverser.traverser_match import TraverserMatch


class RootMatch(TraverserMatch):
    __slots__ = ()

    @property
    def path_as_list(self) -> list:
        return [self]

    @property
    def path(self) -> str:
        return self.real_data_name

    @property
    def path_segment(self) -> str:
        return self.real_data_name

    def traverse(self, visit: typing.Callable[[TraverserMatch], None]):
        visit(self)

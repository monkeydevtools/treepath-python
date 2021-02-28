import typing

from treepath.path.traverser.traverser_match import TraverserMatch


class ImaginaryMatch(TraverserMatch):
    """
    An ImaginaryMatch purpose defines additional traversing state without moving the pointer to the vertex in the data tree
    structure.  The traversing algorithms use this object to assist in traversing the data tree structure without
    mangling the real_parent traversing state.
    """
    __slots__ = ()

    @property
    def path_as_list(self) -> list:
        return [self]

    @property
    def path(self) -> str:
        return self.real_parent.path

    @property
    def path_segment(self) -> str:
        return self.real_parent.path_segment

    @property
    def parent(self):
        return self.real_parent.parent

    def traverse(self, visit: typing.Callable):
        """
        Skip to the real_parent.  This get_match has
        """
        self.real_parent.traverse(visit)

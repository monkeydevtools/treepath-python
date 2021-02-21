import typing

from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class EmptyMatch(TraverserStateMatch):
    """
    An EmptyMatch purpose defines additional traversing state without moving the pointer to the vertex in the data tree
    structure.  The traversing algorithms use this object to assist in traversing the data tree structure without
    mangling the parent traversing state.
    """
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
        return self._parent.path

    @property
    def path_segment(self):
        return self._parent.path_segment

    @property
    def parent(self):
        return self._parent.parent

    def traverse(self, visit: typing.Callable):
        """
        Skip to the parent.  This match has
        """
        self._parent.traverse(visit)

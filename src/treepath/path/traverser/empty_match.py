import typing

from treepath.path.traverser.match import Match


class EmptyMatch(Match):
    """
    An EmptyMatch purpose defines additional traversing state without moving the pointer to the vertex in the data tree
    structure.  The traversing algorithms use this object to assist in traversing the data tree structure without
    mangling the parent traversing state.
    """

    def __init__(self, parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action):
        super().__init__(parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action)
        self._path_as_list = [self]

    @property
    def path_as_list(self) -> list:
        return self._path_as_list

    @property
    def path(self):
        return self.parent.path

    def path_segment(self):
        return self.parent.path_segment()

    def traverse(self, visit: typing.Callable):
        """
        Skip to the parent.  This match has
        """
        self.parent.traverse(visit)

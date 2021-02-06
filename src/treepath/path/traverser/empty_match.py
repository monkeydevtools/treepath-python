import typing

from treepath.path.traverser.match import Match


class EmptyMatch(Match):

    def __init__(self, parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action):
        super().__init__(parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action)
        self._path_as_list = [self]

    @property
    def path_as_list(self) -> list:
        return self._path_as_list

    @property
    def path(self):
        return self.data_name

    def path_segment(self):
        return self.data_name

    def traverse(self, visit: typing.Callable):
        self.parent.traverse(visit)

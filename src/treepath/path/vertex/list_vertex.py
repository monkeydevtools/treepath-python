from abc import ABC

from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class ListVertex(Vertex, ABC):

    def __init__(self, parent, name):
        super().__init__(parent, name)

    def path_segment(self):
        return f"[{self.name}]"


class ListIndexVertex(ListVertex):
    def __init__(self, parent, index: int):
        self.index = index
        super().__init__(parent, index)

    def match(self, parent_match: Match, traverser) -> Match:
        data = parent_match.data
        if not isinstance(data, list):
            return None
        try:
            index = self.index
            value = data[index]
            return ListMatch(
                parent_match,
                index,
                value,
                self,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except IndexError:
            pass


class ListSliceVertex(ListVertex):
    def __init__(self, parent, slice_: slice):
        self._slice = slice_
        super().__init__(parent, slice_)
        self.is_catch_vertex = True

    def path_segment(self):
        slice_ = self._slice
        start = slice_.start
        if not start:
            start = ''
        stop = slice_.stop
        if not stop:
            stop = ''
        step = slice_.step
        if not step:
            return f"[{start}:{stop}]"
        return f"[{start}:{stop}:{step}]"

    def match(self, parent_match: Match, traverser) -> object:

        remembered_catch_state = parent_match.remembered_catch_state

        # create a slice iterator  if there is none
        if not remembered_catch_state:
            data = parent_match.data
            if not isinstance(data, list):
                return None
            remembered_catch_state = enumerate(data[self._slice])
            traverser.remember_on_catch(parent_match, remembered_catch_state)

        try:
            item = next(remembered_catch_state)
            return ListMatch(
                parent_match,
                item[0],
                item[1],
                self,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None


class ListWildVertex(ListVertex):
    def __init__(self, parent):
        super().__init__(parent, '*')
        self.is_catch_vertex = True

    def path_segment(self):
        return "[*]"

    def match(self, parent_match: Match, traverser) -> object:

        remembered_catch_state = parent_match.remembered_catch_state

        # create a list iterator  if there is none
        if not remembered_catch_state:
            data = parent_match.data
            if not isinstance(data, list):
                return None
            remembered_catch_state = enumerate(data)
            traverser.remember_on_catch(parent_match, remembered_catch_state)

        try:
            item = next(remembered_catch_state)
            return ListMatch(
                parent_match,
                item[0],
                item[1],
                self,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None

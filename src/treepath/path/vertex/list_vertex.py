from abc import abstractmethod
from typing import Union

from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.util.function import enumerate_slice
from treepath.path.vertex.vertex import Vertex


class _ListVertex(Vertex):
    __slots__ = ()

    def __init__(self, parent, name):
        super().__init__(parent, name)

    @property
    def path_segment(self):
        return f"[{self.name}]"

    @abstractmethod
    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:
        raise NotImplementedError


class ListIndexVertex(_ListVertex):
    __slots__ = 'index'

    def __init__(self, parent, index: int):
        self.index = index
        super().__init__(parent, index)

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:
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
                vertex_index,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except IndexError:
            pass


class ListSliceVertex(_ListVertex):
    __slots__ = '_slice'

    def __init__(self, parent, slice_: slice):
        self._slice = slice_
        super().__init__(parent, slice_)
        self.is_catch_vertex = True

    @property
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

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        remembered_catch_state = parent_match.remembered_catch_state

        # create a slice iterator  if there is none
        if not remembered_catch_state:
            data = parent_match.data
            if not isinstance(data, list):
                return None
            remembered_catch_state = enumerate_slice(self._slice, data)
            traverser.remember_on_catch(parent_match, remembered_catch_state)

        try:
            item = next(remembered_catch_state)
            return ListMatch(
                parent_match,
                item[0],
                item[1],
                self,
                vertex_index,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None


class ListWildVertex(_ListVertex):
    __slots__ = ()

    def __init__(self, parent):
        super().__init__(parent, '*')
        self.is_catch_vertex = True

    @property
    def path_segment(self):
        return "[*]"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

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
                vertex_index,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None

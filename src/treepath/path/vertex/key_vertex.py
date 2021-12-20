from typing import Union

from treepath.path.traverser.key_match import KeyMatch
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.typing.json_types import JsonTypes
from treepath.path.vertex.vertex import Vertex


class KeyVertex(Vertex):
    __slots__ = ()

    def __init__(self, parent, name):
        super().__init__(parent, name)

    @property
    def path_segment(self):
        return f".{self.name}"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:
        data = parent_match.data
        if not isinstance(data, dict):
            return None
        try:
            name = self.name
            value = data[self.name]
            return KeyMatch(
                parent_match,
                name,
                value,
                self,
                vertex_index,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except KeyError:
            pass

    @property
    def default_value_for_set(self) -> Union[dict, list]:
        return dict()

    def set(self, parent_match: TraverserMatch, value: JsonTypes) -> TraverserMatch:
        data = parent_match.data
        if isinstance(data, dict):
            data[self.name] = value
            return self.match(parent_match, None, parent_match.vertex_index + 1)
        else:
            self.raise_invalid_set(data, value)

    def pop(self, match: TraverserMatch) -> JsonTypes:
        data = match.parent.data
        if isinstance(data, dict):
            return data.pop(self.name)
        else:
            self.raise_invalid_pop(data)


class KeyWildVertex(Vertex):
    __slots__ = ()

    def __init__(self, parent):
        super().__init__(parent, '*')
        self.is_catch_vertex = True

    @property
    def path_segment(self):
        return ".*"

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        remembered_catch_state = parent_match.remembered_catch_state

        # create a dict iterator  if there is none
        if not remembered_catch_state:
            data = parent_match.data
            if not isinstance(data, dict):
                return None
            remembered_catch_state = iter(data.items())
            traverser.remember_on_catch(parent_match, remembered_catch_state)

        try:
            item = next(remembered_catch_state)
            return KeyMatch(
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

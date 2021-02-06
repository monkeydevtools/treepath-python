import functools

from treepath.path.traverser.empty_match import EmptyMatch
from treepath.path.traverser.key_match import KeyMatch
from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class CatchState:
    def __init__(self, iterable, match_constructor):
        self.iterable = iterable
        self.match_constructor = match_constructor
        self.last_match = None


class RecursiveVertex(Vertex):
    def __init__(self, parent):
        super().__init__(parent, ".")
        self.is_catch_vertex = True

    def path_segment(self):
        return f"."

    @functools.cached_property
    def path(self):
        return ''.join(vertex.path_segment() for vertex in self.path_as_list) + "."

    def match(self, parent_match: Match, traverser) -> object:

        remembered_catch_state = parent_match.remembered_catch_state
        if not remembered_catch_state:
            remembered_catch_state = self._create_on_catch_state(parent_match)
            if not remembered_catch_state:
                return None
            traverser.remember_on_catch(parent_match, remembered_catch_state)

            if parent_match.vertex == self.parent and self != traverser.leaf_vertex:
                match = EmptyMatch(
                    parent_match,
                    "EmptyMatch",
                    parent_match.data,
                    self,
                    parent_match.remembered_on_catch_match,
                    parent_match.remembered_on_catch_action
                )
                remembered_catch_state.last_match = match
                return match

        try:
            item = next(remembered_catch_state.iterable)
            parent_match.remembered_on_catch_action = traverser.recursive_match_action
            match = remembered_catch_state.match_constructor(
                parent_match,
                item[0],
                item[1],
                self,
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
            remembered_catch_state.last_match = match
            return match

        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None

    def recursive_match(self, parent_match: Match) -> object:
        remembered_catch_state = parent_match.remembered_catch_state
        last_match = remembered_catch_state.last_match
        match = remembered_catch_state.match_constructor(
            parent_match,
            last_match.data_name,
            last_match.data,
            self,
            parent_match.remembered_on_catch_match,
            parent_match.remembered_on_catch_action
        )
        return match

    def _create_on_catch_state(self, parent_match: Match):
        data = parent_match.data
        if isinstance(data, dict):
            return self._key_match(parent_match)
        elif isinstance(data, list):
            return self._list_match(parent_match)
        else:
            return None

    @staticmethod
    def _key_match(parent_match: Match) -> CatchState:
        iterable = iter(parent_match.data.items())
        return CatchState(iterable, KeyMatch)

    @staticmethod
    def _list_match(parent_match: Match) -> CatchState:
        iterable = iter(enumerate(parent_match.data))
        return CatchState(iterable, ListMatch)

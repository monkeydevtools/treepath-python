from typing import Union

from treepath.path.traverser.key_match import KeyMatch
from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.traverser_match import TraverserMatch


class CatchState:
    __slots__ = 'iterable', \
                'match_constructor'

    def __init__(self, iterable, match_constructor):
        self.iterable = iterable
        self.match_constructor = match_constructor


class GenericWildcardVertex:
    __slots__ = ()

    def match(self, parent_match: TraverserMatch, traverser, vertex_index: int) -> Union[TraverserMatch, None]:

        remembered_catch_state = parent_match.remembered_catch_state
        if not remembered_catch_state:
            remembered_catch_state = self._create_on_catch_state(parent_match)
            if not remembered_catch_state:
                return None
            traverser.remember_on_catch(parent_match, remembered_catch_state)

        try:
            item = next(remembered_catch_state.iterable)

            return remembered_catch_state.match_constructor(
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

    def _create_on_catch_state(self, parent_match: TraverserMatch):
        data = parent_match.data
        if isinstance(data, dict):
            return self._key_match(parent_match)
        elif isinstance(data, list):
            return self._list_match(parent_match)
        else:
            return None

    @staticmethod
    def _key_match(parent_match: TraverserMatch) -> CatchState:
        iterable = iter(parent_match.data.items())
        return CatchState(iterable, KeyMatch)

    @staticmethod
    def _list_match(parent_match: TraverserMatch) -> CatchState:
        iterable = iter(enumerate(parent_match.data))
        return CatchState(iterable, ListMatch)

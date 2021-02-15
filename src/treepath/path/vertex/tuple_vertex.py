from treepath.path.traverser.key_match import KeyMatch
from treepath.path.traverser.list_match import ListMatch
from treepath.path.traverser.match import Match
from treepath.path.vertex.vertex import Vertex


class CatchState:
    __slots__ = 'iterable', \
                'match_constructor'

    def __init__(self, iterable, match_constructor):
        self.iterable = iterable
        self.match_constructor = match_constructor


class TupleVertex(Vertex):
    __slots__ = '_tuple'

    def __init__(self, parent, tuple_: tuple):
        self._tuple = tuple_
        super().__init__(parent, tuple_)
        self.is_catch_vertex = True

    def path_segment(self):
        return repr(self._tuple)

    def match(self, parent_match: Match, traverser) -> object:

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
                parent_match.remembered_on_catch_match,
                parent_match.remembered_on_catch_action
            )
        except StopIteration:
            traverser.restore_on_catch(parent_match)
            return None

    def _create_on_catch_state(self, parent_match: Match):
        data = parent_match.data
        if isinstance(data, dict):
            return self._key_match(parent_match)
        elif isinstance(data, list):
            return self._list_match(parent_match)
        else:
            return None

    def _key_match(self, parent_match: Match) -> CatchState:
        tuple__ = self._tuple

        def my_iter():
            tuple_ = tuple__
            data = parent_match.data
            for key in tuple_:
                try:
                    value = data[key]
                    yield key, value
                except KeyError:
                    continue

        iterable = my_iter()
        return CatchState(iterable, KeyMatch)

    def _list_match(self, parent_match: Match) -> CatchState:
        tuple__ = self._tuple

        def my_iter():
            tuple_ = tuple__
            data = parent_match.data
            for index in tuple_:
                try:
                    value = data[index]
                    yield index, value
                except (IndexError, TypeError):
                    continue

        iterable = my_iter()
        return CatchState(iterable, ListMatch)

from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.typing.json_types import JsonTypes


class ValueTraverser(MatchTraverser):
    __slots__ = ()

    def __next__(self) -> JsonTypes:
        return super().__next__().data

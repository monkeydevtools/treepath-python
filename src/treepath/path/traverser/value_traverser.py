from treepath.path.traverser.match_traverser import MatchTraverser
from treepath.path.typing_alias import JsonTypes


class ValueTraverser(MatchTraverser):
    __slots__ = ()

    def __next__(self) -> JsonTypes:
        return super().__next__().data

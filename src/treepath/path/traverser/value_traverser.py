from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser


class ValueTraverser(MatchTraverser):
    __slots__ = ()

    def __next__(self) -> Match:
        return super().__next__().data

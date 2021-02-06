from treepath.path.traverser.match import Match
from treepath.path.traverser.match_traverser import MatchTraverser


class ValueTraverser(MatchTraverser):

    def __next__(self) -> Match:
        return super().__next__().data

from treepath.path.traverser.match_traverser import MatchTraverser


class ValueTraverser(MatchTraverser):
    __slots__ = ()

    def __next__(self) -> object:
        return super().__next__().data

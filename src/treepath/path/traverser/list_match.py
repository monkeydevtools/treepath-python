from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class ListMatch(TraverserStateMatch):
    __slots__ = ()

    @property
    def path_segment(self):
        return f"[{self.data_name}]"

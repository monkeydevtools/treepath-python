from treepath.path.traverser.traverser_match import TraverserMatch


class ListMatch(TraverserMatch):
    __slots__ = ()

    @property
    def path_segment(self):
        return f"[{self.real_data_name}]"

from treepath.path.traverser.traverser_match import TraverserMatch


class ParentMatch(TraverserMatch):
    __slots__ = '_remembered_parent'

    def __init__(self, remembered_parent, *args):
        super().__init__(*args)
        self._remembered_parent = remembered_parent

    @property
    def path_segment(self) -> str:
        return f"<-{self.real_data_name}"

    @property
    def remembered_parent(self):
        return self._remembered_parent.parent

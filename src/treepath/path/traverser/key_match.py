from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class KeyMatch(TraverserStateMatch):
    __slots__ = ()

    def __init__(self,
                 parent,
                 data_name, data,
                 vertex,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        TraverserStateMatch.__init__(self,
                                     parent,
                                     data_name,
                                     data,
                                     vertex,
                                     remembered_on_catch_match,
                                     remembered_on_catch_action
                                     )

    @property
    def path_segment(self):
        return f".{self.data_name}"

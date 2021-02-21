from treepath.path.traverser.match import Match


class TraverserStateMatch(Match):
    __slots__ = 'vertex_index', \
                'remembered_catch_state', \
                'remembered_on_catch_match', \
                'remembered_on_catch_action'

    def __init__(self,
                 parent,
                 data_name,
                 data, vertex,
                 remembered_on_catch_match,
                 remembered_on_catch_action
                 ):
        Match.__init__(self,
                       parent,
                       data_name,
                       data,
                       vertex
                       )
        self.vertex_index = 0
        self.remembered_catch_state = None
        self.remembered_on_catch_match = remembered_on_catch_match
        self.remembered_on_catch_action = remembered_on_catch_action

    @property
    def path_segment(self):
        raise NotImplementedError

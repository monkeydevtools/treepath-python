from treepath.path.traverser.match import Match


class ListMatch(Match):

    def __init__(self, parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action):
        super().__init__(parent, data_name, data, vertex, remembered_on_catch_match, remembered_on_catch_action)

    def path_segment(self):
        return f"[{self.data_name}]"

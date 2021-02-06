from treepath.path.vertex.vertex import Vertex


class TreepathException(Exception):
    """Basic exception for errors raised by treepath"""

    def __init__(self, vertex: Vertex):
        self.vertex = vertex
        self.is_msg_resolved = False
        super().__init__()

    def __repr__(self):
        if self.is_msg_resolved:
            return self.msg
        self.msg = self._resolve_msg()
        return self.msg

    def __str__(self):
        return self.__repr__()

    def _resolve_msg(self):
        self.is_msg_resolved = True
        path = repr(self.vertex)
        return f"TreepathException on path: {path}"

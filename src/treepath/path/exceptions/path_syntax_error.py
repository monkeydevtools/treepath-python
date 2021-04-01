import os

from treepath.path.exceptions.treepath_exception import TreepathException
from treepath.path.vertex.vertex import Vertex


class PathSyntaxError(TreepathException, SyntaxError):
    """PathSyntaxError is raised when there is an syntax issue with the path"""

    def __init__(self, vertex: Vertex, error_msg, invalid_path_segment):
        self.error_msg = error_msg
        self.invalid_path_segment = invalid_path_segment
        super().__init__(vertex)

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"""PathSyntaxError({self.error_msg}{os.linesep}  path: {path}{self.invalid_path_segment})"""

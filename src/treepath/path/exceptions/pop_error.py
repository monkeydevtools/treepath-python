import os
from typing import Union

from treepath.path.exceptions.treepath_exception import TreepathException
from treepath.path.vertex.vertex import Vertex


class PopError(TreepathException, SyntaxError, LookupError):
    """PopError is raised when there is a issue setting a value"""

    def __init__(self, parent_vertex: Union[Vertex, None], error_msg, invalid_path_segment):
        self.error_msg = error_msg
        self.invalid_path_segment = invalid_path_segment
        super().__init__(parent_vertex)

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"PopError({self.error_msg}{os.linesep}  path: {path}{self.invalid_path_segment})"

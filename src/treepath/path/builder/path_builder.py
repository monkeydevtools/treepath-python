from typing import Union, Callable, Match, Any

from treepath.path.builder.abstract_class_builder import AbstractPathBuilder
from treepath.path.builder.patch_constants import wildcard
from treepath.path.builder.path_builder_predicate import PathBuilderPredicate
from treepath.path.builder.symbol import Symbol
from treepath.path.exceptions.path_syntax_error import PathSyntaxError
from treepath.path.vertex.key_vertex import KeyVertex, KeyWildVertex
from treepath.path.vertex.list_vertex import ListIndexVertex, ListSliceVertex, ListWildVertex
from treepath.path.vertex.parent_vertex import ParentVertex
from treepath.path.vertex.predicate_vertex import PredicateVertex
from treepath.path.vertex.recursive_vertex import RecursiveVertex
from treepath.path.vertex.tuple_vertex import TupleVertex
from treepath.path.vertex.vertex import Vertex

_RESERVED_ATTR_FOR_VERTEX_DATA = "_RESERVED_ATTR_FOR_VERTEX_DATA"
"""
  _RESERVED_ATTR_FOR_VERTEX_DATA:  A special attribute name used by PathBuilder to store all the DATA related to the 
  vertex.   It purpose keep data attribute separate from PathBuilder in order to reduce attribute name collision.  
"""


def _build_key(parent_vertex: Vertex, key: Union[int, slice, Symbol, str, tuple, Callable[[Match], Any]]):
    if isinstance(key, int):
        return ListIndexVertex(parent_vertex, key)
    elif isinstance(key, slice):
        return ListSliceVertex(parent_vertex, key)
    if wildcard == key:
        return ListWildVertex(parent_vertex)
    elif isinstance(key, str):
        return KeyVertex(parent_vertex, key)
    elif isinstance(key, tuple):
        return TupleVertex(parent_vertex, key)
    elif callable(key):
        return PredicateVertex(parent_vertex, key)
    else:
        raise PathSyntaxError(parent_vertex,
                              f"Unsupported indices: [{type(key)}].  Indices must be either an int, slice, tuple, "
                              f"str, wildcard, has(function), or callable.",
                              f"[{key}]"
                              )


class PathBuilder(PathBuilderPredicate, AbstractPathBuilder):
    __slots__ = _RESERVED_ATTR_FOR_VERTEX_DATA

    def __init__(self, vertex, ):
        object.__setattr__(self, _RESERVED_ATTR_FOR_VERTEX_DATA, vertex)

    def __getattr__(self, name):
        """
        creates a new attribute at self.
        This method only get called if self.name does not already exist
        self.name
        """
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = KeyVertex(parent_vertex, self.tranform_attribute_name(name))
        path_builder = self.create_path_builder(vertex)
        return path_builder

    def __setattr__(self, name, value):
        """
        Overloads self.name = value
        Attribute assignment not supported.
        """
        raise AttributeError(f"set __setattr__  {name} {value} not supported on {self.__name__}")

    def __getitem__(self, key: Union[int, slice, Symbol, str, tuple, Callable[[Match], Any]]):
        """
        Overloads self[key]
        """
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = _build_key(parent_vertex, key)
        path_builder = self.create_path_builder(vertex)
        return path_builder

    def __setitem__(self, key, value):
        """
        Overloads self[key]=value
        """
        raise AttributeError(f"set __setitem__  {key} not supported on {self.__name__}")

    def __repr__(self):
        vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        return repr(vertex)

    def __str__(self):
        vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        return str(vertex)

    def __len__(self):
        """ Always return 0 as the [] is used as a factory and not a fetch"""
        return 0

    @property
    def shape(self):
        """
        The attribute name shape is reserved. Use path["shape"] instead of path.shape',

        Debuggers expect a property named shape to be defined when a class also defines a __getitem__.   The dynamite
        attribute defined by __getattr__ conflicts with the value the debugger expects the shape property to return.
        This can causes instability with some debuggers.

        To prevent any instability with debuggers, the property shape is reserved so it cannot be used a a dynamic
        property.
        """
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        raise PathSyntaxError(
            parent_vertex,
            'The attribute name shape is reserved. Use path["shape"] instead of path.shape.',
            ".shape"
        )

    def create_path_builder(self, *args, **kwargs):
        return PathBuilder(*args, **kwargs)

    def tranform_attribute_name(self, name):
        return name

    @property
    def recursive(self):
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = RecursiveVertex(parent_vertex)
        if isinstance(parent_vertex, RecursiveVertex):
            raise PathSyntaxError(
                parent_vertex,
                "Successive recursive vertices are not allowed in the path expression.",
                ".."
            )
        path_builder = self.create_path_builder(vertex)
        return path_builder

    @property
    def rec(self):
        return self.recursive

    @property
    def wildcard(self):
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = KeyWildVertex(parent_vertex)
        path_builder = self.create_path_builder(vertex)
        return path_builder

    @property
    def wc(self):
        return self.wildcard

    @property
    def parent(self):
        parent_vertex = object.__getattribute__(self, _RESERVED_ATTR_FOR_VERTEX_DATA)
        vertex = ParentVertex(parent_vertex)
        path_builder = self.create_path_builder(vertex)
        return path_builder


def get_vertex_from_path_builder(path_builder: PathBuilder) -> Vertex:
    vertex = object.__getattribute__(path_builder, _RESERVED_ATTR_FOR_VERTEX_DATA)
    return vertex

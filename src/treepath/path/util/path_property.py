from typing import Union, Callable, Any

from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.match import Match
from treepath.path.traverser.traverser_functions import get, set_
from treepath.path.traverser.traverser_functions import get_match


def pprop(path: PathBuilder,
          get_data: Union[property, Callable[[Any], Union[dict, list, str, int, float, bool, None]]]
          ):
    """
       Creates Path Property used to get and set json attribute

       example:

       class ExamplePathProperty:
           def __init__(self, data_):
               self._data = data_
           @property
           def data(self) -> dict:
               return self._data

           a_b_c = pprop(path.a.b.c, data)

       data = {"a": {"b": {"c": 1}}}
       epp = ExamplePathProperty(data)
       assert epp.a_b_c == 1
       epp.a_b_c = 2
       assert epp.a_b_c == 2
    """
    return PathProperty(path, get_data)


def mprop(path: PathBuilder,
          get_data: Union[property, Callable[[Any], Union[dict, list, str, int, float, bool, None]]]
          ):
    """
    Similar to pprop exect the getter  return a Match
    """
    return MatchPathProperty(path, get_data)


class PathProperty:
    __slots__ = '_get_data', \
                '_path'

    def __init__(self,
                 path: PathBuilder,
                 get_data: Union[property, Callable[[Any], Union[dict, list, str, int, float, bool, None]]]
                 ):
        self._path = path
        self._set_get_data(get_data)

    def _set_get_data(self, get_data):
        """
        Determine how data, is a callable, property or a descriptor.
        """
        if callable(get_data):
            self._get_data = get_data
        elif isinstance(get_data, property):
            self._get_data = get_data.fget
        elif hasattr(get_data, '__get__'):
            def getter(instance):
                return get_data.__get__(instance, None)

            self._get_data = getter
        else:
            raise AttributeError(f"Cannot invoke f{get_data}") # pragma: no cover

    def get_value(self, outer_self):
        return get(self._path, self._get_data(outer_self), default=None)

    def get_match(self, outer_self) -> Match:
        return get_match(self._path, self._get_data(outer_self), must_match=False)

    def set_value(self, outer_self, value):
        set_(self._path, value, self._get_data(outer_self))

    def __get__(self, instance, owner) -> Union[dict, list, str, int, float, bool, None]:
        return self.get_value(instance)

    def __set__(self, instance, value: Union[dict, list, str, int, float, bool, None]):
        return self.set_value(instance, value)


class MatchPathProperty(PathProperty):

    def __init__(self, path: PathBuilder,
                 get_data: Union[property, Callable[[Any], Union[dict, list, str, int, float, bool, None]]]):
        super().__init__(path, get_data)

    def __get__(self, instance, owner) -> Match:
        return self.get_match(instance)

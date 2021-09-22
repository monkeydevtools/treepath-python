from typing import Union, Callable, Any

from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_


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


class PathProperty(property):
    __slots__ = '_get_data', \
                '_path', \
                '__doc__',

    def __init__(self,
                 path: PathBuilder,
                 get_data: Union[property, Callable[[Any], Union[dict, list, str, int, float, bool, None]]]
                 ):
        super().__init__(self.get_value, self.set_value, self.del_value)
        self._path = path
        if isinstance(get_data, property):
            self._get_data = get_data.fget
        else:
            self._get_data = get_data

    def get_value(self, outer_self):
        return get(self._path, self._get_data(outer_self), default=None)

    def set_value(self, outer_self, value):
        set_(self._path, value, self._get_data(outer_self))

    def del_value(self, outer_self):
        raise NotImplementedError  # pragma: no cover

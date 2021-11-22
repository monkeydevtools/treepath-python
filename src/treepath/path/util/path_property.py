from abc import ABC
from typing import Union, Callable, Any

from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.match import Match
from treepath.path.traverser.traverser_functions import get, set_, _not_set, set_match
from treepath.path.traverser.traverser_functions import get_match
from treepath.path.typing_alias import JsonTypes


class AbstractProperty(ABC):
    pass


GetDataTypes = Union[property, AbstractProperty, Callable[[Any], JsonTypes]]


class PathProperty(AbstractProperty):
    __slots__ = '_get_data', \
                '_path', \
                '_cascade', \
                'default'

    def __init__(self,
                 path: PathBuilder,
                 get_data: GetDataTypes,
                 cascade: bool = False,
                 default=_not_set
                 ):
        self._path = path
        self._set_get_data(get_data)
        self._cascade = cascade
        self.default = default

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
            raise AttributeError(f"Cannot invoke f{get_data}")  # pragma: no cover

    def get_value(self, outer_self):
        return get(self._path, self._get_data(outer_self), default=self.default)

    def set_value(self, outer_self, value):
        set_(self._path, value, self._get_data(outer_self), cascade=self._cascade)

    def __get__(self, instance, owner) -> JsonTypes:
        return self.get_value(instance)

    def __set__(self, instance, value: JsonTypes):
        self.set_value(instance, value)


class MatchPathProperty(PathProperty):
    __slots__ = 'must_match'

    def __init__(self, path: PathBuilder,
                 get_data: GetDataTypes,
                 must_match: bool = True,
                 **kwards
                 ):
        self.must_match = must_match
        super().__init__(path, get_data, **kwards)

    def get_match(self, outer_self) -> Match:
        return get_match(self._path, self._get_data(outer_self), must_match=self.must_match)

    def set_match(self, outer_self, value: Union[Match, JsonTypes]):
        set_match(self._path, value, self._get_data(outer_self), cascade=self._cascade)

    def __get__(self, instance, owner) -> Match:
        return self.get_match(instance)

    def __set__(self, instance, value: Union[Match, JsonTypes]):
        self.set_match(instance, value)


def prop(
        path: PathBuilder,
        get_data: GetDataTypes,
        cascade: bool = False,
        default=_not_set
) -> PathProperty:
    """
       Creates Path Property used to get and set json attribute

       example:

       class ExamplePathProperty:
           def __init__(self, data_):
               self._data = data_
           @property
           def data(self) -> dict:
               return self._data

           a_b_c = prop(path.a.b.c, data)

       data = {"a": {"b": {"c": 1}}}
       epp = ExamplePathProperty(data)
       assert epp.a_b_c == 1
       epp.a_b_c = 2
       assert epp.a_b_c == 2
    """
    return PathProperty(path, get_data, cascade=cascade, default=default)


def propm(
        path: PathBuilder,
        get_data: GetDataTypes,
        cascade: bool = False,
        must_match: bool = True,
) -> MatchPathProperty:
    """
    Similar to prop except the getter returns a Match
    """
    return MatchPathProperty(path, get_data, cascade=cascade, must_match=must_match)

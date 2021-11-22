from typing import Union, TypeVar

JsonTypes = Union[dict, list, str, int, float, bool, None]

JsonTypeVar = TypeVar('JsonTypeVar', dict, list, str, int, float, bool, type(None))

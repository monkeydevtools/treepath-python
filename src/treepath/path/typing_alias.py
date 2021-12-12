from typing import Union, TypeVar, Dict, List

JsonTypes = Union[Dict[str, 'JsonTypes'], List['JsonTypes'], str, int, float, bool, None]

JsonTypeVar = TypeVar('JsonTypeVar', Dict[str, JsonTypes], List[JsonTypes], str, int, float, bool, type(None))

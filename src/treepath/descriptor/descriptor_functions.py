from __future__ import annotations

from typing import Callable, Union, Any, Type, Optional

from treepath.descriptor.descriptor_builder import DescriptorBuilder
from treepath.descriptor.path_descriptor import PathDescriptor
from treepath.descriptor.path_descriptor import T
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_, find, get_match, find_matches, set_match
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing


def attr(expression: Optional[PathBuilder] = None,
         *,
         getter: Union[get, find, get_match, find_matches] = get,
         setter: Union[set_, set_match] = set_,
         to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
         to_json_value: Callable[[Any], JsonTypes] = do_nothing
         ) -> PathDescriptor[T]:
    """
    Constructs a descriptor to be attached to a subclass of a Document.

    class X(Document):
        a = attr()

    x = X({"a": 1})
    assert x.a == 1

    @param expression: The path expression that define the search criteria. The expression is optional.  The default
      value is the attribute name the descriptor is being assigned too.
    @param getter: The treepath traverser function used to fetch the value from the Document.
    @param setter: The treepath traverser function used to assign the value to the Document.
    @param to_wrapped_value: The treepath function used to unmarshal the value fetch using the getter
    @param to_json_value: The treepath function used to marshal the value to be assigned using the setter.

    @return PathDescriptor:  Returns a path descriptor configured as specified by the parameters.
    """
    return PathDescriptor(
        expression=expression,
        getter=getter,
        setter=setter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
    )


def attr_typed(type_: Type[T],
               expression: Optional[PathBuilder] = None,
               *,
               getter: Union[get, find, get_match, find_matches] = get,
               setter: Union[set_, set_match] = set_,
               to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
               to_json_value: Callable[[Any], JsonTypes] = do_nothing
               ) -> PathDescriptor[T]:
    """
    Constructs Typed descriptor to be attached to a subclass of a treepath Document.

    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_typed(X)

    y = Y({"b": {"a": 1}})
    assert y.b.a == 1

    @param type_: The attribute type.  The type can be either subclass of treepath Document or a custom type.  The
    to_wrapped_value and to_json_value must be defined for custom type.
    @param expression: The path expression that define the search criteria. The expression is optional.  The default
      value is the attribute name the descriptor is being assigned too.
    @param getter: The treepath traverser function used to fetch the value from the Document.
    @param setter: The treepath traverser function used to assign the value to the Document.
    @param to_wrapped_value: The treepath function used to unmarshal the value fetch using the getter.  The argument
      must be specified for custom types.
    @param to_json_value: The treepath function used to marshal the value to be assigned using the setter.  The
      argument must be specified for custom types.
    @return PathDescriptor:  Returns a path descriptor configured as specified by the parameters.
    """
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        expression=expression,
        getter=getter,
        setter=setter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
    )
    return descriptor_builder.build_single()


def attr_iter_typed(type_: Type[T],
                    expression: Optional[PathBuilder] = None,
                    *,
                    getter: Union[find, find_matches] = find,
                    to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
                    ) -> PathDescriptor[T]:
    """
    Constructs Typed iterator descriptor to be attached to a subclass of a treepath Document.

    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_iter_typed(X, path.b[wc])

    y = Y({"b": [{"a": 1}, {"a": 2}]})
    x = iter(y.b)
    assert next(x).a == 1
    assert next(x).a == 2

    @param type_: The attribute type.  The type can be either subclass of treepath Document or a custom type.  The
    to_wrapped_value and to_json_value must be defined for custom type.
    @param expression: The path expression that define the search criteria. The expression is optional.  The default
      value is the attribute name the descriptor is being assigned too.
    @param getter: The treepath traverser function used to fetch the value from the Document.
    @param to_wrapped_value: The treepath function used to unmarshal the value fetch using the getter.  The argument
      must be specified for custom types.
    @return PathDescriptor:  Returns a path descriptor configured as specified by the parameters.
    """
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        expression=expression,
        getter=getter,
        to_wrapped_value=to_wrapped_value,
    )
    return descriptor_builder.build_iterator()


def attr_list_typed(type_: Type[T],
                    expression: Optional[PathBuilder] = None,
                    *,
                    getter: Union[get, get_match] = get,
                    to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
                    to_json_value: Callable[[Any], JsonTypes] = do_nothing
                    ) -> PathDescriptor[T]:
    """
    Constructs Typed list descriptor to be attached to a subclass of a treepath Document.

    class X(Document):
        a = attr()

    class Y(Document):
        b = attr_list_typed(X, path.b)

    y = Y({"b": [{"a": 1}, {"a": 2}]})
    assert y.b[0].a == 1
    assert y.b[1].a == 2

    @param type_: The attribute type.  The type can be either subclass of treepath Document or a custom type.  The
    to_wrapped_value and to_json_value must be defined for custom type.
    @param expression: The path expression that define the search criteria. The expression is optional.  The default
      value is the attribute name the descriptor is being assigned too.
    @param getter: The treepath traverser function used to fetch the value from the Document.
    @param to_wrapped_value: The treepath function used to unmarshal the value fetch using the getter.  The argument
      must be specified for custom types.
    @param to_json_value: The treepath function used to marshal the value to be assigned using the setter.  The
      argument must be specified for custom types.
    @return PathDescriptor:  Returns a path descriptor configured as specified by the parameters.
    """
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        expression=expression,
        getter=getter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
        is_for_json_list=True
    )
    return descriptor_builder.build_list()

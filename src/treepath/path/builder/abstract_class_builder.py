from abc import abstractmethod, ABC


class AbstractPathBuilder(ABC):
    __slots__ = ()

    @abstractmethod
    def create_path_builder(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def tranform_attribute_name(self, name):
        raise NotImplementedError

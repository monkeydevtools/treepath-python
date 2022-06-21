

class AbstractPathBuilder:
    __slots__ = ()

    def create_path_builder(self, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover

    def tranform_attribute_name(self, name):
        raise NotImplementedError  # pragma: no cover

class Storage:
    """Storage determines technique to store components,"""

    def __init__(self):
        pass

    def insert(self, entity, component):
        raise NotImplementedError

    def get(entity):
        raise NotImplementedError


class DictStorage(Storage):
    """DictStorage uses entities as keys to components."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.components = {}

    def get(self, key):
        return self.components[key]

    def insert(self, key, value):
        self.components[key] = value


class PackedStorage(Storage):
    """PackedStorage stores components sequentially."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components = []

    def insert(self, key, value):
        # Entities should not have multiple of same component
        self.components.append((key, value))

        def get(entity):
            for _entity, component in self.components:
                if _entity == entity:
                    return component

            raise IndexError

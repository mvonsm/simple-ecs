class Storage:
    """Storage determines technique to store components."""

    def insert(self, entity: 'Entity', component: 'Component'):
        """Store a specific entity's component."""
        raise NotImplementedError

    def get(self, entity: 'Entity') -> 'Component':
        """Get an entity's component from storage."""
        raise NotImplementedError

    def delete(self, entity: 'Entity'):
        """Delete an entity's component from storage."""
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

    def get(self, entity):
        for _entity, component in self.components:
            if _entity == entity:
                return component

        raise IndexError

    def insert(self, key, value):
        # Entities should not have multiple of same component
        self.components.append((key, value))

from typing import Tuple


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

    def items(self) -> Tuple['Entity', 'Component']:
        """Generator for components."""


class DictStorage(Storage):
    """DictStorage uses entities as keys to components."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components = {}

    def get(self, key):
        return self.components[key]

    def insert(self, key, value):
        self.components[key] = value

    def delete(self, key):
        del self.components[key]

    def items(self):
        for key, value in self.components.item():
            yield key, value


class ListStorage(Storage):
    """PackedStorage stores components sequentially."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components = []

    def get(self, entity):
        for _entity, component in self.items():
            if _entity == entity:
                return component

        raise IndexError

    def insert(self, key, value):
        # Entities should not have multiple of same component
        self.components.append((key, value))

    def delete(self, entity):
        for i in range(len(self.componenents)):
            _entity, _ = self.components[i]

            if _entity == entity:
                del self.components[i]
                return

    def items(self):
        for entity, component in self.components:
            yield entity, component


class PackedStorage(ListStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = 0

    def items(self):
        size = len(self.components)
        for _ in range(size):
            entity, component = self.components[self.index % size]
            self.index += 1
            yield entity, component


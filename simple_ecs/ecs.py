from typing import Callable
from enum import Enum

from .storage import DictStorage, PackedStorage


class Component:
    """Component is a property of an entity."""

    storage = DictStorage

    def __init__(self):
        raise NotImplementedError


class Entity:
    """Entity represents an object in the store."""

    def __init__(self):
        self.component_types = set()


class Store:
    """Storage for entities, components, and the connections between them."""

    def __init__(self):
        self.components = {}
        self.entities = []
        self.callbacks = []

    def create_entity(self):
        entity = Entity()
        self.entities.append(entity)
        return entity

    def assign(self, entity: Entity, component: Component):

        entity.component_types.add(component.__class__)
        storage = self.components.setdefault(
            component.__class__, component.__class__.storage()
        )
        storage.insert(entity, component)

    def get_components(self):
        raise NotImplementedError

    def _get_ent_components(self, ent, component_types):

        result = []
        for ctype in component_types:
            result.append(self.components[ctype].get(ent))

        return result

    def _handle_callback(self, callback):

        for ent in self.entities:
            if set(callback.args).issubset(ent.component_types):
                result = self._get_ent_components(ent, callback.args)
                callback.callback(*result)

    def update(self):
        for callback in self.callbacks:
            self._handle_callback(callback)


class ComponentSystem:
    """ComponentSystem decorates a function to act on entity properties."""

    def __init__(self, store: Store, *args):
        self.store = store
        self.args = args

    def __call__(self, callback):
        self.callback = callback
        self.store.callbacks.append(self)
        return callback

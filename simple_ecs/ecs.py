from typing import Callable
from enum import Enum


class Storage(Enum):
    """Storage enum to identify how component should be stored."""

    DEFAULT = 1
    PACKED = 2
    DUPLICATE = 3


class Component:
    """Component is a property of an entity."""

    storage = Storage.DEFAULT

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

        if component.storage in (Storage.DEFAULT, Storage.DUPLICATE):
            some_dict = self.components.setdefault(component.__class__, {})
            some_dict[hash(entity)] = component

        if component.storage in (Storage.PACKED, Storage.DUPLICATE):
            self.components.setdefault(component.__class__, []).append(
                (entity, component)
            )

    def get_components(self):
        for component_type in self.components.keys():
            yield component_type, self.components[component_type]

    def _update_components(self, component_type, components):
        if component_type.storage == Storage.DEFAULT:
            pass

    def _get_ent_components(self, ent, component_types):

        result = []
        for ctype in component_types:

            # Temporary until custom storage methods are implemented
            if ctype.storage in (Storage.PACKED, Storage.DUPLICATE):

                for _ent, elem in self.components[ctype]:
                    if _ent == ent:
                        result.append(elem)
                        break

            elif ctype.storage == Storage.DEFAULT:
                result.append(self.components[ctype][hash(ent)])

        return tuple(result)

    def _handle_callback(self, callback):

        for ent in self.entities:
            if not set(callback.args).issubset(ent.component_types):
                continue

            result = self._get_ent_components(ent, callback.args)

            callback.callback(*result)

    def update(self):
        for callback in self.callbacks:
            self._handle_callback(callback)


#  Can likely be consolidated into one class
class ComponentCallback:
    """ComponentCallback is a wrapper for functions set to be called when store updates."""

    def __init__(self, callback: Callable, ctypes):
        self.callback = callback
        self.args = ctypes


class ComponentSystem:
    """ComponentSystem decorates a function to act on entity properties."""

    def __init__(self, store: Store, *args):
        self.store = store
        self.component_types = args

    def __call__(self, callback):
        self.callback = callback
        self.store.callbacks.append(
            ComponentCallback(callback, self.component_types)
        )
        return callback

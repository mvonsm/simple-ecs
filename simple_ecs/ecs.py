from typing import Callable, Type, List, Tuple

from .storage import Storage, DictStorage, PackedStorage


class Component:
    """Component is a property of an entity."""

    storage: Type[Storage] = DictStorage

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

    def create_entity(self) -> Entity:
        """Creates and registers new entity in the store."""
        entity = Entity()
        self.entities.append(entity)
        return entity

    def assign(self, entity: Entity, component: Component):
        """Assign a component to an entity.
        
        :param entity: The :class:`Entity <Entity>` to assign the :class:`Component <Component>` to.
        :param component: The component to assign.

        """

        entity.component_types.add(component.__class__)
        storage = self.components.setdefault(
            component.__class__, component.__class__.storage()
        )
        storage.insert(entity, component)

    def _get_ent_components(
        self, entity: Entity, component_types: Tuple[Type[Component]]
    ) -> List[Component]:

        """Returns the components of an entity.

        :param entity: The :class:`Entity <Entity>` to get components of.
        :param component_types: Tuple of Component derived types.
        """

        result = []
        for ctype in component_types:
            result.append(self.components[ctype].get(entity))

        return result

    def _handle_callback(
        self, callback: Callable, component_types: Tuple[Type[Component]]
    ):
        """Prepares callback arguments, then calls with those arguments.
        :param callback: The system to call.
        :param component_types: Tuple of Component derived types.

        """

        for ent in self.entities:
            if set(component_types).issubset(ent.component_types):
                result = self._get_ent_components(ent, component_types)
                callback(*result)

    def update(self):
        """Call all registered update functions."""
        for callback, component_types in self.callbacks:
            self._handle_callback(callback, component_types)


class ComponentSystem:
    """ComponentSystem decorates a function to act on entity properties."""

    def __init__(self, store: Store, *args):
        self.store = store
        self.args = args

    def __call__(self, callback: Callable):
        self.callback = callback
        self.store.callbacks.append((self.callback, self.args))
        return callback

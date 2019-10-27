class Entity:
    def __init__(self, registry, *componenents):
        self.registry = registry
        self.components = *componenents

class Component:
    '''A generic component. '''

    def __init__(self):
        raise NotImplementedError

    def update(self, entity):
        return 0


class ComponentHandler:
    def __init__(self, registry, component_class):
        self.registry = registry
        self.component_class = component_class

    def __call__(self, callback):
        self.callback = callback

        self.registry.callbacks.setdefault(self.component_class, []).append(
            callback
        )
        return callback


class Registry:
    def __init__(self):
        self.reg = {}
        self.ent_reg = {}
        self.ent_class_reg = {}

        self.callbacks = {}
        self.count = 0

    def create_entity(self):
        return Entity(self.count)

    def assign(self, entity: Entity, component: Component):

        if not issubclass(component.__class__, Component):
            raise TypeError

        # Components sequentially NOTE: may be faster to iterate through deserialized
        self.reg.setdefault(component.__class__, []).append(
            (entity, component)
        )

        # Components by entity
        self.ent_reg.setdefault(entity, set()).add(component)

        # Component classes by entity
        self.ent_class_reg.setdefault(entity, set()).add(component.__class__)


    def faster_update(self):
        for comp_type in self.reg:5
            for ent, component in self.reg[comp_type]:


                

    def update(self):
        def call_all(callbacks, args):
            for cb in callbacks:
                cb(args)

        for comp_type, callbacks in self.callbacks.items():

            temp_type = comp_type
            is_list = False

            if isinstance(comp_type, tuple):
                is_list = True
                temp_type = comp_type[0]

            for entity, component in self.reg[temp_type]:

                _component = component
                if is_list and set(comp_type).issubset(
                    self.ent_class_reg[entity]
                ):
                    _component = self.ent_reg[entity]

                call_all(callbacks, _component)

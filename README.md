# simple-ecs

*Note: simple-ecs is still in active development, and not yet ready to be used.*

A simple to use entity component system. As this project progresses it'll become more customizable.

Basic Example
-------

```py
from simple_ecs import Store, Component, ComponentSystem, Storage

store = Store()

class PositionComponent(Component):
    storage = Storage.PACKED

    def __init__(self, x, y):
        self.x = x
        self.y = y

@ComponentSystem(store, PositionComponent)
def handleinput(position):
    position.x += 1
    position.y += 1

ent = store.create_entity()
store.assign(ent, PositionComponent(0, 0))

while True:
    store.update()
```

Links
--------
**TBA**

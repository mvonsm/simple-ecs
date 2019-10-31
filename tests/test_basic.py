import pytest
from simple_ecs import Store, Component, ComponentSystem, DictStorage


@pytest.fixture
def store():
    return Store()


class MoveComponent(Component):
    storage = DictStorage

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class MassComponent(Component):
    def __init__(self, mass):
        self.mass = mass


def test_basic(store: Store):
    @ComponentSystem(store, MoveComponent)
    def handleinput(result):

        assert result.__class__ == MoveComponent
        print(result)

    ent = store.create_entity()
    store.assign(ent, MoveComponent(0, 0, 0))
    store.update()


def test_multiple(store: Store):
    @ComponentSystem(store, MoveComponent, MassComponent)
    def handleinput(position, mass):
        assert position.__class__ == MoveComponent
        assert mass.__class__ == MassComponent

        print(f"position {position} mass {mass}")

    ent = store.create_entity()
    store.assign(ent, MoveComponent(0, 0, 0))
    store.assign(ent, MassComponent(100))
    store.update()

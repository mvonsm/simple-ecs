import pytest
from simple_ecs import Store, Component, ComponentSystem, Storage


@pytest.fixture
def store():
    return Store()


class MoveComponent(Component):
    storage = Storage.DEFAULT

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def test_increment(store: Store):
    @ComponentSystem(store, MoveComponent)
    def handleinput(result):

        assert result.__class__ == MoveComponent
        print(result)

    ent = store.create_entity()
    store.assign(ent, MoveComponent(0, 0, 0))
    store.update()

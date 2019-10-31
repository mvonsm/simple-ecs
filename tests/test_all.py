import pytest
from simple_ecs import (
    Store,
    Component,
    ComponentSystem,
    DictStorage,
    PackedStorage,
)


@pytest.fixture
def store():
    return Store()


class ArgComponent(Component):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class DictStorageComponent(ArgComponent):
    storage = DictStorage


class PackedStorageComponent(ArgComponent):
    storage = PackedStorage


def test_basic_dictstorage(store):

    total = 100000
    for i in range(total):
        ent = store.create_entity()
        store.assign(ent, DictStorageComponent(0, 0, 0))

    count = 0

    @ComponentSystem(store, DictStorageComponent)
    def handleinput(dscomp):
        nonlocal count
        count += 1

    store.update()
    assert count == total


def test_basic_packedstorage(store):

    total = 100000
    for i in range(total):
        ent = store.create_entity()
        store.assign(ent, PackedStorageComponent(0, 0, 0))

    count = 0

    @ComponentSystem(store, PackedStorageComponent)
    def handleinput(dscomp):
        nonlocal count
        count += 1

    store.update()
    assert count == total


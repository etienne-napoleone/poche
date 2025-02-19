from datetime import datetime, timedelta

from poche import Item


def test_new_with_no_expiration():
    item = Item(value="test", expiration=None)
    assert item.value == "test"
    assert not item.expiration


def test_new_with_expiration():
    expiration = datetime.now() + timedelta(minutes=1)
    item = Item(value="test", expiration=expiration)
    assert item.value == "test"
    assert isinstance(item.expiration, datetime)
    assert item.expiration > datetime.now()


def test_repr():
    item = Item("test", None)
    assert f"{item}" == 'Item("test", None)'
    item = Item(5, None)
    assert f"{item}" == "Item(5, None)"
    now = datetime.now()
    item = Item("test", now)
    assert f"{item}" == f'Item("test", {now})'


def test_is_expired():
    expiration = datetime.now() + timedelta(minutes=1)
    item = Item(value="test", expiration=expiration)
    assert not item.is_expired()
    expiration = datetime.now()
    item = Item(value="test", expiration=expiration)
    assert item.is_expired()

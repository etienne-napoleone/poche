from datetime import datetime, timedelta

import pytest

from poche import Cache, Item


def test_new_with_no_ttl():
    cache = Cache()
    assert cache._items == {}
    assert not cache.ttl


def test_new_with_int_ttl():
    cache = Cache(ttl=60)
    assert cache._items == {}
    assert isinstance(cache.ttl, timedelta)
    assert cache.ttl == timedelta(seconds=60)


def test_new_with_timedelta_ttl():
    cache = Cache(ttl=timedelta(seconds=60))
    assert cache._items == {}
    assert isinstance(cache.ttl, timedelta)
    assert cache.ttl == timedelta(seconds=60)


def test_new_with_ttl_typeerror():
    with pytest.raises(TypeError):
        Cache(ttl="str")
    with pytest.raises(TypeError):
        Cache(ttl=True)


def test_magic_delitem():
    cache = Cache()
    item = Item(value="test", expiration=None)
    cache._items["one"] = item
    del cache["one"]
    assert not cache._items.get("one")


def test_magic_getitem_with_existent_item():
    cache = Cache()
    item = Item(value="test", expiration=None)
    cache._items["one"] = item
    assert cache["one"] == "test"


def test_magic_getitem_with_non_existent_item():
    cache = Cache()
    with pytest.raises(KeyError):
        cache["one"]


def test_get_expiration_with_no_ttl():
    cache = Cache()
    assert not cache._get_expiration_from_ttl(ttl=None)
    cache = Cache(ttl=60)
    planned = datetime.now()
    expiration = cache._get_expiration_from_ttl(ttl=None)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1


def test_get_expiration_with_int_ttl():
    cache = Cache()
    delta = 10
    planned = datetime.now() + timedelta(seconds=delta)
    expiration = cache._get_expiration_from_ttl(ttl=delta)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    planned = datetime.now() + timedelta(seconds=delta)
    expiration = cache._get_expiration_from_ttl(ttl=delta)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1


def test_get_expiration_with_timedelta_ttl():
    cache = Cache()
    delta = timedelta(seconds=10)
    planned = datetime.now() + delta
    expiration = cache._get_expiration_from_ttl(ttl=delta)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    delta = timedelta(seconds=10)
    planned = datetime.now() + delta
    expiration = cache._get_expiration_from_ttl(ttl=delta)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1


def test_get_expiration_with_datetime_ttl():
    cache = Cache()
    planned = datetime.now() + timedelta(seconds=10)
    expiration = cache._get_expiration_from_ttl(ttl=planned)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    planned = datetime.now() + timedelta(seconds=10)
    expiration = cache._get_expiration_from_ttl(ttl=planned)
    assert isinstance(expiration, datetime)
    assert expiration.second < planned.second + 1
    assert expiration.second > planned.second - 1


def test_get_expiration_with_ttl_typeerror():
    cache = Cache()
    with pytest.raises(TypeError):
        assert cache._get_expiration_from_ttl(ttl="test")
    with pytest.raises(TypeError):
        assert cache._get_expiration_from_ttl(ttl=True)


def test_get_with_no_expiration():
    cache = Cache()
    item = Item(value="test", expiration=None)
    cache._items["one"] = item
    assert cache.get("one") == "test"


def test_get_with_expiration_not_expired():
    cache = Cache()
    item = Item(value="test", expiration=datetime.now() + timedelta(seconds=60))
    cache._items["one"] = item
    assert cache.get("one") == "test"


def test_get_with_expiration_expired():
    cache = Cache()
    item = Item(value="test", expiration=datetime.now())
    cache._items["one"] = item
    assert not cache.get("one")


def test_set_with_no_ttl():
    cache = Cache()
    cache.set("one", "test")
    assert cache._items["one"].value == "test"


def test_set_with_int_ttl():
    cache = Cache()
    planned = datetime.now()
    cache.set("one", "test", ttl=0)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    planned = datetime.now()
    cache.set("one", "test", ttl=0)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1


def test_set_with_timedelta_ttl():
    cache = Cache()
    delta = timedelta(seconds=10)
    planned = datetime.now() + delta
    cache.set("one", "test", ttl=delta)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    delta = timedelta(seconds=10)
    planned = datetime.now() + delta
    cache.set("one", "test", ttl=delta)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1


def test_set_with_datetime_ttl():
    cache = Cache()
    planned = datetime.now()
    cache.set("one", "test", ttl=planned)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1
    cache = Cache(ttl=60)
    planned = datetime.now()
    cache.set("one", "test", ttl=planned)
    assert cache._items["one"].value == "test"
    assert cache._items["one"].expiration.second < planned.second + 1
    assert cache._items["one"].expiration.second > planned.second - 1


def test_getset():
    cache = Cache()
    item = Item(value="test", expiration=None)
    cache._items["one"] = item
    assert cache.getset("one", "test2") == "test"
    assert cache._items["one"].value == "test2"


def test_flush():
    cache = Cache()
    item_one = Item(value="test", expiration=None)
    item_two = Item(value="test", expiration=None)
    cache._items["one"] = item_one
    cache._items["two"] = item_two
    assert len(cache._items.keys()) == 2
    cache.flush()
    assert cache._items == {}

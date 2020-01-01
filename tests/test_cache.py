from datetime import datetime
from datetime import timedelta
import time

import pytest

from poche.cacheitem import Cacheitem

TTL = 3600
DATETIME = datetime.now() + timedelta(days=1)
KEY = "test_key"
VALUE = 1
VALUE_ITEM = Cacheitem(None, VALUE)
VALUE_ITEM_TTL = Cacheitem(datetime.now(), VALUE)


def test_set(cache):
    cache.set(KEY, VALUE)
    assert cache._store[KEY] == VALUE_ITEM


def test_set_default_ttl(cache_default_ttl):
    cache_default_ttl.set(KEY, VALUE)
    time.sleep(2)
    with pytest.raises(KeyError):
        assert cache_default_ttl.get(KEY) == VALUE_ITEM


def test_set_key_not_hashable(cache):
    with pytest.raises(TypeError):
        assert cache.set({}, VALUE)


def test_set_with_ttl(cache):
    cache.set(KEY, VALUE, ttl=TTL)
    assert isinstance(cache._store[KEY].expiration, datetime)


def test_get(cache):
    cache._store[KEY] = VALUE_ITEM
    assert cache.get(KEY) == VALUE


def test_get_key_not_hashable(cache):
    with pytest.raises(TypeError):
        assert cache.get({})


def test_get_raises_keyerror(cache):
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_get_with_ttl(cache):
    cache._store[KEY] = Cacheitem(DATETIME, VALUE)
    assert cache.get(KEY) == VALUE


def test_get_ttl_expirationd(cache):
    cache._store[KEY] = VALUE_ITEM_TTL
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_gos_get(cache):
    cache._store[KEY] = VALUE_ITEM
    assert cache.gos(KEY, VALUE) == VALUE


def test_gos_set(cache):
    assert cache.gos(KEY, VALUE) == VALUE
    assert cache._store[KEY] == VALUE_ITEM


def test_set_ttl(cache):
    cache._store[KEY] = Cacheitem(None, 1)
    assert not cache._store[KEY].expiration
    cache.set_ttl(KEY, 1)
    assert isinstance(cache._store[KEY].expiration, datetime)


def test_set_ttl_datetime(cache):
    cache._store[KEY] = Cacheitem(None, 1)
    assert not cache._store[KEY].expiration
    cache.set_ttl(KEY, datetime.now())
    assert isinstance(cache._store[KEY].expiration, datetime)


def test_get_ttl(cache):
    cache._store[KEY] = Cacheitem(None, 1)
    assert not cache.get_ttl(KEY)
    cache._store[KEY] = Cacheitem(datetime.now(), 1)
    assert isinstance(cache.get_ttl(KEY), datetime)


def test_bump(cache):
    now = datetime.now()
    cache._store[KEY] = Cacheitem(now, 1)
    cache.bump(KEY, 1)
    assert cache._store[KEY].expiration > now


def test_bump_no_ttl(cache):
    cache._store[KEY] = Cacheitem(None, 1)
    cache.bump(KEY, 1)
    assert not cache._store[KEY].expiration


def test_delete(cache):
    cache._store[KEY] = VALUE_ITEM
    cache.delete(KEY)
    with pytest.raises(KeyError):
        assert cache._store[KEY] == VALUE


def test_delete_raises_keyerror(cache):
    with pytest.raises(KeyError):
        assert cache.delete(KEY)


def test_keys(cache):
    cache._store[KEY] = VALUE_ITEM
    assert list(cache.keys()) == [KEY]


def test_values(cache):
    cache._store[KEY] = VALUE_ITEM
    assert list(cache.values()) == [VALUE_ITEM]


def test_items(cache):
    cache._store[KEY] = VALUE_ITEM
    assert list(cache.items()) == [(KEY, VALUE_ITEM)]


def test_flush(cache):
    cache._store[KEY] = "test"
    cache.flush()
    with pytest.raises(KeyError):
        assert cache._store[KEY]


def test_get_expiration(cache):
    end = cache._get_expiration(TTL)
    assert end > datetime.now()


def test_get_expiration_datetime(cache):
    end = cache._get_expiration(DATETIME)
    assert end > datetime.now()
    assert end == DATETIME


def test_get_expiration_no_ttl(cache):
    assert not cache._get_expiration(None)


def test_get_expiration_default_ttl(cache_default_ttl):
    end = cache_default_ttl._get_expiration(TTL)
    assert end > datetime.now()
    time.sleep(2)
    assert end > datetime.now()


def test_get_expiration_default_ttl_no_ttl(cache_default_ttl):
    end = cache_default_ttl._get_expiration(None)
    assert end > datetime.now()
    time.sleep(2)
    assert end < datetime.now()


def test_expire(cache):
    item = Cacheitem(DATETIME, 1)
    cache._store[KEY] = Cacheitem(DATETIME, 1)
    cache._expire(KEY, item)


def test_expire_raises_keyerror(cache):
    cache._store[KEY] = VALUE_ITEM_TTL
    with pytest.raises(KeyError):
        cache._expire(KEY, VALUE_ITEM_TTL)


def test_magic_len(cache):
    cache._store[KEY] = VALUE_ITEM
    assert len(cache) == 1


def test_magic_getitem(cache):
    cache._store[KEY] = VALUE_ITEM
    assert cache[KEY] == VALUE_ITEM


def test_magic_setitem(cache):
    cache[KEY] = VALUE_ITEM
    assert cache._store[KEY] == VALUE_ITEM


def test_magic_setitem_raises_typeerror(cache):
    with pytest.raises(TypeError):
        cache[KEY] = "value"


def test_magic_delitem(cache):
    cache._store[KEY] = VALUE_ITEM
    del cache[KEY]
    with pytest.raises(KeyError):
        assert cache._store[KEY]


def test_magic_delitem_raises_keyerror(cache):
    with pytest.raises(KeyError):
        del cache[KEY]


def test_magic_contains(cache):
    cache._store[KEY] = VALUE_ITEM
    assert KEY in cache
    assert "absent_key" not in cache


def test_magic_contains_raises_typeerror(cache):
    with pytest.raises(TypeError):
        assert {} in cache

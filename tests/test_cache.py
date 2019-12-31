from datetime import datetime
from datetime import timedelta
import time

import pytest

from poche.cacheitem import Cacheitem

TTL = 3600
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


def test_set_ttl(cache):
    cache.set(KEY, VALUE, ttl=TTL)
    assert isinstance(cache._store[KEY].expiration, datetime)


def test_get(cache):
    cache._store[KEY] = VALUE_ITEM
    assert cache.get(KEY) == VALUE


def test_get_key_not_hashable(cache):
    with pytest.raises(TypeError):
        assert cache.get({})


def test_get_absent(cache):
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_get_ttl(cache):
    cache._store[KEY] = Cacheitem(datetime.now() + timedelta(days=1), VALUE)
    assert cache.get(KEY) == VALUE


def test_get_ttl_expirationd(cache):
    cache._store[KEY] = VALUE_ITEM_TTL
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_get_or_set_get(cache):
    cache._store[KEY] = VALUE_ITEM
    assert cache.get_or_set(KEY, VALUE) == VALUE


def test_get_or_set_set(cache):
    assert cache.get_or_set(KEY, VALUE) == VALUE
    assert cache._store[KEY] == VALUE_ITEM


def test_delete(cache):
    cache._store[KEY] = VALUE_ITEM
    cache.delete(KEY)
    with pytest.raises(KeyError):
        assert cache._store[KEY] == VALUE


def test_delete_absent(cache):
    with pytest.raises(KeyError):
        assert cache.delete(KEY)


def test_flush(cache):
    cache._store[KEY] = "test"
    cache.flush()
    with pytest.raises(KeyError):
        assert cache._store[KEY]


def test_get_expiration(cache):
    end = cache._get_expiration(TTL)
    assert end > datetime.now()
    time.sleep(2)
    assert end > datetime.now()


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

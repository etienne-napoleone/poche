from datetime import datetime
from datetime import timedelta
import time

import pytest

TTL = 3600
KEY = "test_key"
VALUE = 1
VALUE_TUPLE = (None, VALUE)
VALUE_TUPLE_TTL = (datetime.now(), VALUE)


def test_set(cache):
    cache.set(KEY, VALUE)
    assert cache._store[KEY] == VALUE_TUPLE


def test_set_default_ttl(cache_default_ttl):
    cache_default_ttl.set(KEY, VALUE)
    time.sleep(2)
    with pytest.raises(KeyError):
        assert cache_default_ttl.get(KEY) == VALUE_TUPLE


def test_set_key_not_hashable(cache):
    with pytest.raises(TypeError):
        assert cache.set({}, VALUE)


def test_set_ttl(cache):
    cache.set(KEY, VALUE, ttl=TTL)
    assert isinstance(cache._store[KEY][0], datetime)


def test_get(cache):
    cache._store[KEY] = VALUE_TUPLE
    assert cache.get(KEY) == VALUE


def test_get_key_not_hashable(cache):
    with pytest.raises(TypeError):
        assert cache.get({})


def test_get_absent(cache):
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_get_ttl(cache):
    cache._store[KEY] = (datetime.now() + timedelta(days=1), VALUE)
    assert cache.get(KEY) == VALUE


def test_get_ttl_expired(cache):
    cache._store[KEY] = VALUE_TUPLE_TTL
    with pytest.raises(KeyError):
        assert cache.get(KEY)


def test_get_or_set_get(cache):
    cache._store[KEY] = VALUE_TUPLE
    assert cache.get_or_set(KEY, VALUE) == VALUE


def test_get_or_set_set(cache):
    assert cache.get_or_set(KEY, VALUE) == VALUE
    assert cache._store[KEY] == VALUE_TUPLE


def test_delete(cache):
    cache._store[KEY] = VALUE_TUPLE
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

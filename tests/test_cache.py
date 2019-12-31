from datetime import datetime
from datetime import timedelta
import time

import pytest

from poche.cache import Cache

TTL = 3600
KEY = "test_key"
VALUE = 1
VALUE_TUPLE = (None, VALUE)
VALUE_TUPLE_TTL = (datetime.now(), VALUE)


def test_set():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE_TUPLE
    Cache._store = {}


def test_set_key_not_str():
    with pytest.raises(TypeError):
        assert Cache.set(1, VALUE)
    Cache._store = {}


def test_set_override():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE_TUPLE
    Cache.set(KEY, "override")
    assert Cache._store[KEY] == (None, "override")
    Cache._store = {}


def test_set_override_disabled():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE_TUPLE
    Cache.set(KEY, "override", override=False)
    assert Cache._store[KEY] == VALUE_TUPLE
    Cache._store = {}


def test_set_ttl():
    Cache.set(KEY, VALUE, ttl=TTL)
    assert isinstance(Cache._store[KEY][0], datetime)
    Cache._store = {}


def test_get():
    Cache._store[KEY] = VALUE_TUPLE
    assert Cache.get(KEY) == VALUE
    Cache._store = {}


def test_get_key_not_str():
    with pytest.raises(TypeError):
        assert Cache.get(1)
    Cache._store = {}


def test_get_absent():
    with pytest.raises(KeyError):
        assert Cache.get(KEY)
    Cache._store = {}


def test_get_ttl():
    Cache._store[KEY] = (datetime.now() + timedelta(days=1), VALUE)
    assert Cache.get(KEY) == VALUE
    Cache._store = {}


def test_get_ttl_expired():
    Cache._store[KEY] = VALUE_TUPLE_TTL
    with pytest.raises(KeyError):
        assert Cache.get(KEY)
    Cache._store = {}


def test_ttl():
    Cache.set(KEY, VALUE, TTL)
    time.sleep(1)
    assert Cache.get(KEY)
    Cache._store = {}


def test_ttl_expire():
    Cache.set(KEY, VALUE, 1)
    time.sleep(2)
    with pytest.raises(KeyError):
        assert Cache.get(KEY)
    Cache._store = {}


def test_flush():
    Cache._store[KEY] = "test"
    Cache.flush()
    with pytest.raises(KeyError):
        assert Cache._store[KEY]
    Cache._store = {}


def test_get_expiration():
    assert Cache._get_expiration_dt(TTL) > datetime.now()
    Cache._store = {}

from poche.cache import Cache

KEY = "test_key"
VALUE = 1
VALUE_TUPLE = (None, VALUE)


def test_set():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE_TUPLE
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


def test_get():
    Cache._store[KEY] = VALUE_TUPLE
    assert Cache.get(KEY) == VALUE
    Cache._store = {}


def test_get_absent():
    assert not Cache.get(KEY)

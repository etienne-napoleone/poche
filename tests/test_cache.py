from poche.cache import Cache

KEY = "test_key"
VALUE = 1


def test_set():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE
    Cache._store = {}


def test_set_override():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE
    Cache.set(KEY, "override")
    assert Cache._store[KEY] == "override"
    Cache._store = {}


def test_set_override_disabled():
    Cache.set(KEY, VALUE)
    assert Cache._store[KEY] == VALUE
    Cache.set(KEY, "override", override=False)
    assert Cache._store[KEY] == VALUE
    Cache._store = {}


def test_get():
    Cache._store[KEY] = VALUE
    assert Cache.get(KEY) == VALUE
    Cache._store = {}

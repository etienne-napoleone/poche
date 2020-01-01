from datetime import datetime

import pytest

from poche.cacheitem import Cacheitem

ITEM = Cacheitem(datetime.now(), 1)


def test_instantiate():
    assert ITEM.expiration
    assert ITEM.value


def test_magic_eq():
    assert ITEM == ITEM
    assert ITEM == Cacheitem(None, 1)
    assert ITEM == 1
    assert not ITEM == "1"


def test_magic_ne():
    assert not ITEM != ITEM
    assert not ITEM != Cacheitem(None, 1)
    assert not ITEM != 1
    assert ITEM != "1"


def test_magic_lt():
    assert ITEM < Cacheitem(None, 2)
    assert ITEM < 2
    assert not ITEM < 0
    with pytest.raises(TypeError):
        assert ITEM < "2"


def test_magic_gt():
    assert ITEM > Cacheitem(None, 0)
    assert ITEM > 0
    assert not ITEM > 2
    with pytest.raises(TypeError):
        assert ITEM > "0"


def test_magic_le():
    assert ITEM <= Cacheitem(None, 2)
    assert ITEM <= 2
    assert ITEM <= Cacheitem(None, 1)
    assert ITEM <= 1
    assert not ITEM <= 0
    with pytest.raises(TypeError):
        assert ITEM <= "2"


def test_magic_ge():
    assert ITEM >= Cacheitem(None, 0)
    assert ITEM >= 0
    assert ITEM >= Cacheitem(None, 1)
    assert ITEM >= 1
    assert not ITEM >= 2
    with pytest.raises(TypeError):
        assert ITEM >= "0"

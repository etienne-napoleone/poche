from datetime import datetime

from poche.cacheitem import Cacheitem


def test_instantiate():
    item = Cacheitem(datetime.now(), "value")
    assert item.expiration
    assert item.value

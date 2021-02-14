from datetime import datetime
from datetime import timedelta


from poche import TTLItem


def test_init_no_ttl():
    item = TTLItem(value="test")
    assert item.value == "test"
    assert not item.ttl


def test_init_datetime():
    ttl = datetime.now() + timedelta(weeks=100)
    item = TTLItem(value="test", ttl=ttl)
    assert item.value == "test"
    assert item.ttl == ttl


def test_init_timedelta():
    ttl = timedelta(weeks=100)
    item = TTLItem(value="test", ttl=ttl)
    assert item.value == "test"
    assert item.ttl > datetime.now()

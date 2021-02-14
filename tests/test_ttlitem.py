from datetime import datetime

from poche import TTLItem


def test_ttlcache_item():
    expiration = datetime.now()
    item = TTLItem(expiration=expiration, value="test")
    assert item.value == "test"
    assert item.expiration == expiration

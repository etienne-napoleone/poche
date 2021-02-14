def test_getset_absent(cache):
    item = cache.getset(1, "test")
    assert not item
    assert cache.data[1] == "test"

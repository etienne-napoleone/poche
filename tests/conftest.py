import pytest

from poche import Cache


@pytest.fixture
def cache():
    return Cache()


@pytest.fixture
def cache_default_ttl():
    return Cache(default_ttl=1)

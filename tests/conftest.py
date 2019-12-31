import pytest

from poche import Cache


@pytest.fixture
def cache():
    return Cache()

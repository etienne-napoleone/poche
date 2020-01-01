# poche

[![Build Status](https://travis-ci.org/etienne-napoleone/poche.svg?branch=develop)](https://travis-ci.org/etienne-napoleone/poche)
[![Codecov](https://codecov.io/gh/etienne-napoleone/poche/branch/develop/graph/badge.svg)](https://codecov.io/gh/etienne-napoleone/poche)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple and fast Python in-memory caching.

Meant to speed up using dictionaries as cache backend for simple usecases.

No external dependencies, 100% code coverage and static type checked.

## Installation

Requires Python 3.6+.

```bash
pip install poche
```

## Roadmap

v1:

- [x] K/V cache system
- [x] Basic TTL
- [x] TTL methods (get, bump, remove, etc)
- [ ] Memoizing decorator
- [ ] (Lower required Python version)

v2:

- [ ] Optional per cache stats

## Usage

Instantiate a Poche cache object:

```python
>>> import poche
>>> c = poche.Cache()
# or you can set a default TTL
>>> c = poche.Cache(default_ttl=5)
```

**Warning:** When using TTLs, The only call removing a value with expired TTL is `get()`!

### Basic operations

Set a value in cache:

```python
def set(key: Hashable, value: Any, Optional: Optional[Union[int, datetime]] = None) -> None
```

Get a value in cache:

```python
def get(key: Hashable) -> Any
```

Get or set a value in cache if not present:

```python
def gos(key: Hashable, value: Any, ttl: Optional[int] = None) -> Any
```

Delete a value in cache:

```python
def delete(key: Hashable) -> None
```

Flush all cache content:

```python
def flush() -> None
```

Examples:

```python
>>> c.set("un", 1)
>>> c.get("un")
1
>>> c.delete("un")

>>> c.get("deux")
KeyError
>>> c.gos("deux", 2) 
2
>>> c.gos("deux", 3)
2
>>> c.get("deux")
2
>>> c.flush()
```

### TTLs

Set the TTL of a cache item:

```python
def set_ttl(key: Hashable, ttl: Optional[Union[int, datetime]],) -> None
```

Get the TTL of a cache item:

```python
def get_ttl(key: Hashable) -> Optional[datetime]
```

Add seconds to the current TTL:

```python
def bump(key: str, ttl: int) -> None:
```
Examples:

```python
>>> c.set("un", 1, ttl=2)
>>> c.get("un")
1
>>> time.sleep(3)
>>> c.get("un")
KeyError

>>> c.set("deux", 2, ttl=datetime(2025, 20, 1)) 
>>> c.get_ttl("deux")
datetime(2025, 20, 1)
>>> c.set_ttl("deux", 2)
>>> time.sleep(3)
>>> c.get("deux")
KeyError

>>> c.set("trois", 3, ttl=2)
>>> c.set_ttl(None)
>>> time.sleep(3)
>>> c.get("trois")
3

# The only call removing a value with expired TTL is `get()`!
>>> c.set("quatre", 4, ttl=2)
>>> time.sleep(3)
>>> "quatre" in c.keys()
True
>>> c.get("quatre")
KeyError
>>> "quatre" in c.keys()
False
```

### Dictionary like methods

Get the cache keys:

```python
def keys() -> KeysView[Hashable]
```

Get de cache values:

```python
def values() -> ValuesView[Any]
```

Get the cache values:

```python
def items() -> ItemsView[Hashable, Cacheitem]
```
Examples:

```python
>>> c.set("un", 1)
>>> c.set("deux", 2)
>>> c.keys()
["un", "deux"]
>>> c.values()
[1, 2]
>>> for item in c.items():
...     print(f"{item[0]} -> {item[1].value}")
"1 -> un"
"2 -> deux"
```

### Access raw objects

Examples:

```Python
>>> c.set("un", 1)
>>> c["un"]
Cacheitem(expiration=None, value=1)
>>> c["un"] == 1
True
>>> 1 in c
True
>>> c["un"] < 2
True
>>> c["deux"] = 2
TypeError
>>> c["deux"] = Cacheitem(expiration=None, value=2)
>>> len(c)
2
>>> c["un"] < c["deux"]
True
>>> del c["deux"]
```

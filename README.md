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
- [ ] TTL methods (get, bump, remove, etc)
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

Get, set, get or set (gos) and delete items:

```python
>>> c.set("un", 1, ttl=5)
>>> c.get("un")
1
>>> time.sleep(5)
>>> c.get("un")
KeyError
>>> c.set("deux", 2, ttl=datetime(2025, 20, 1)) 
>>> c.gos("trois", 3)
2
>>> c.gos("trois", "another value")
2
>>> c.get("trois")
2
>>> c.delete("trois")
>>> c.flush()
```

Dictionary methods:

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

Access raw objects:

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

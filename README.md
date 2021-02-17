# poche

[![Build Status](https://travis-ci.org/etienne-napoleone/poche.svg?branch=develop)](https://travis-ci.org/etienne-napoleone/poche)
[![Codecov](https://codecov.io/gh/etienne-napoleone/poche/branch/develop/graph/badge.svg)](https://codecov.io/gh/etienne-napoleone/poche)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple and fast Python in-memory caching with support for TTLs.

Meant to speed up using dictionaries as cache backend for simple usecases.

No external dependencies, 100% code coverage and static type checked.

## Installation

Requires Python 3.6+.

```bash
pip install poche
```

## Roadmap

v1:

- [x] Basic TTL
- [x] `get`
- [x] `set`
- [x] `getset`
- [ ] `flush`

v1.1:

- [ ] `expire`
- [ ] `persist`
- [ ] `rename`

v1.2:

- [ ] `getorset` with callback

## Example

```python
from time import sleep

import poche

>>> c = poche.Cache()
>>> c = poche.Cache(ttl=5)  # you can also define a default TTL

>>> c.set("one", 1)
>>> c.get("one")
1

>>> c.get("two")
None
>>> c.getset("two", 2)
None
>>> c.get("two")
2

>>> c.set("three", 3, ttl=2)
>>> c.get("three")
3
>>> sleep(2)
>>> c.get("three")
None
```

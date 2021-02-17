# poche

[![Build Status](https://travis-ci.org/etienne-napoleone/poche.svg?branch=main)](https://travis-ci.org/etienne-napoleone/poche)
[![Codecov](https://codecov.io/gh/etienne-napoleone/poche/branch/main/graph/badge.svg)](https://codecov.io/gh/etienne-napoleone/poche)
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
- [x] `flush`

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

>>> c.set("one", "uno")
>>> c.get("one")
"uno"

>>> c.get("two")
None
>>> c.getset("two", "dos")
None
>>> c.get("two")
"dos"

>>> c.set("three", "tres", ttl=2)
>>> c.get("three")
"tres"
>>> sleep(2)
>>> c.get("three")
None

>>> c = poche.Cache(ttl=2)  # you can also define a default TTL

>>> c.set("four", "cuatro")
>>> c.get("four")
"cuatro"
>>> sleep(2)
>>> c.get("four")
None
```

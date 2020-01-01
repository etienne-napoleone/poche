# poche

Simple Python in-memory caching.

Meant to speed up using dictionaries as cache backend for simple usecases.

No external dependencies, requires Python 3.6+.

## Performances

🚧 wip

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
>>> c.gos("deux", 2)
2
>>> c.gos("deux", 3)
2
>>> c.get("deux")
2
>>> c.delete("deux")
# or flush this whole cache
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

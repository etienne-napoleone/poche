# poche

Simple Python dictionary in-memory caching.

No external dependencies, requires Python 3.6+.

## Usage

Set:
```python
>>> from poche import Cache
>>> c = Cache()
>>> c.set("my_key", "my_value")
>>> c.get("my_key")
"my_value"
```

Set with ttl:
```python
>>> from time
>>> from poche import Cache
>>> c = Cache()
>>> c.set("my_key", "my_value", ttl=1)
>>> time.sleep(2)
>>> c.get("my_key")
Traceback (most recent call last):
  ...
KeyError
```

Default ttl:
```python
>>> from time
>>> from poche import Cache
>>> c = Cache(default_ttl=5)
>>> c.set("my_key", "my_value", ttl=1)
>>> time.sleep(2)
>>> c.get("my_key")
Traceback (most recent call last):
  ...
KeyError
>>> c.set("my_key", "my_value")
>>> time.sleep(2)
>>> c.get("my_key")
"my_key"
```

others:
```python
>>> from poche import Cache
>>> c = Cache()
>>> c.flush()  # Flush entire cache
>>> c.get_or_set()  # Get or set with the same signature as set
```

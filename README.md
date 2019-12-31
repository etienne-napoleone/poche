# poche

basic:
```python
>>> from poche import Cache
>>> c = Cache()
>>> c.set("my_key", "my_value")
>>> c.get("my_key")
"my_value"
```

ttl:
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

disable override:
```python
>>> from poche import Cache
>>> c = Cache()
>>> c.set("my_key", "my_value")
>>> c.get("my_key")
"my_value"
>>> c.set("my_key", "another_value", override=False)
>>> c.get("my_key")
"my_value"
```

others:
```python
>>> from poche import Cache
>>> c = Cache()
>>> c.flush()  # Flush entire cache
```

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
>>> c = Cache(default_ttl=5)  # optional default ttl
>>> c.set("my_key", "my_value", ttl=1)  # use specified ttl
>>> time.sleep(2)
>>> c.get("my_key")
Traceback (most recent call last):
  ...
KeyError
>>> c.set("my_key", "my_value")  # use default ttl
>>> time.sleep(2)
>>> c.get("my_key")
"my_key"
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

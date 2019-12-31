# poche

basic:
```python
>>> from poche import Cache
>>> Cache.set("my_key", "my_value")
>>> Cache.get("my_key")
"my_value"
```

ttl:
```python
>>> from time
>>> from poche import Cache
>>> Cache.set("my_key", "my_value", ttl=1)
>>> time.sleep(2)
>>> Cache.get("my_key")
Traceback (most recent call last):
  ...
KeyError
```

disable override:
```python
>>> from poche import Cache
>>> from poche import Cache
>>> Cache.set("my_key", "my_value")
>>> Cache.get("my_key")
"my_value"
>>> Cache.set("my_key", "another_value", override=False)
>>> Cache.get("my_key")
"my_value"
```

# poche

Simple Python dictionary in-memory caching.

No external dependencies, requires Python 3.6+.

## Usage

example with TTLs:

```python
>>> from poche import Cache
>>> import time
>>> c = Cache(default_ttl=5)  # optional `default_ttl`, default to None
>>> c.set("my_key", "my_value", ttl=1)
>>> time.sleep(2)
>>> c.get("my_key")
Traceback (most recent call last):
  ...
KeyError
>>> c.set("my_key", "my_value")  # use default 5s TTL
>>> time.sleep(2)
>>> c.get("my_key")
"my_key"
```

### API

Poche cache is accessed through the `poche.Cache()` class.

#### `Cache()`

**Parameters:**

| Name          | Type          | Default |
|---------------|---------------|---------|
| `default_ttl` | Optional[int] | None    |

**Attributes:**

| Name          | Type          | Default |
|---------------|---------------|---------|
| `default_ttl` | Optional[int] | None    |

**Returns:** None

#### `Cache().set()`

**Parameters:**

| Name    | Type          | Default |
|---------|---------------|---------|
| `key`   | Hashable      | -       |
| `value` | Any           | -       |
| `ttl`   | Optional[int] | None    |

**Raises:**

  - KeyError 

**Returns:** None

#### `Cache().get()`

**Parameters:**
| Name  | Type     | Default |
|-------|----------|---------|
| `key` | Hashable | -       |

**Raises:**

  - KeyError 

**Returns:** Any

#### `Cache().delete()`

**Parameters:**

| Name  | Type     | Default |
|-------|----------|---------|
| `key` | Hashable | -       |

**Raises:**

  - KeyError 

**Returns:** None

#### `Cache().get_or_set()`

**Parameters:**

| Name    | Type          | Default |
|---------|---------------|---------|
| `key`   | Hashable      | -       |
| `value` | Any           | -       |
| `ttl`   | Optional[int] | None    |

**Raises:**

  - KeyError 

**Returns:** Any

#### `Cache().flush()`

**Parameters:** -

**Raises:** -

**Returns:** None

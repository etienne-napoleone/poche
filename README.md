# poche

Simple Python in-memory caching.

Meant to speed up using dictionaries as cache backend for simple usecases.

No external dependencies, requires Python 3.6+.

## Performances

🚧 wip

## Example

Basic:

```python
>>> from poche import Cache
>>> c = Cache()
>>> c.set("my_key", "my_value")
>>> c.get("my_key")
"my_key"
```

Example with TTLs:

```python
>>> from poche import Cache
>>> import time
>>> c = Cache(default_ttl=5)           # optional `default_ttl`, default to None
>>> c.set("my_key", "my_value", ttl=1)
>>> time.sleep(2)
>>> c.get("my_key")
Traceback (most recent call last):
  ...
KeyError
>>> c.set("my_key", "my_value")        # use default 5s TTL
>>> time.sleep(2)
>>> c.get("my_key")
"my_key"
```

## API

Poche cache is accessed through the `poche.Cache()` class.

Each entry is formed by a key and a `poche.Cacheitem()`.

### `Cache()`

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

#### `Cache().delete()`

**Parameters:**

| Name  | Type     | Default |
|-------|----------|---------|
| `key` | Hashable | -       |

**Raises:**

  - KeyError 

**Returns:** None

#### `Cache().keys()`

**Parameters:** -

**Raises:** -

**Returns:** KeysView[Hashable]

#### `Cache().values()`

**Parameters:** -

**Raises:** -

**Returns:** ValuesView[Any]

#### `Cache().items()`

**Parameters:** -

**Raises:** -

**Returns:** ItemsView[Hashable, Cacheitem]

#### `Cache().flush()`

**Parameters:** -

**Raises:** -

**Returns:** None

### `Cacheitem()` (Dataclass)

**Parameters:**

| Name         | Type               | Default |
|--------------|--------------------|---------|
| `expiration` | Optional[datetime] | -       |
| `value`      | Any                | -       |

**Attributes:**

| Name         | Type               | Default |
|--------------|--------------------|---------|
| `expiration` | Optional[datetime] | -       |
| `value`      | Any                | -       |

**Returns:** None

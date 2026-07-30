# Client reference

## `Client`

`Client` stores connection configuration for unauthenticated requests.

```python
from invenio_rest_api_client import Client

client = Client(base_url="https://invenio.example.org")
```

## `AuthenticatedClient`

`AuthenticatedClient` adds token authentication:

```python
from invenio_rest_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url="https://invenio.example.org",
    token="replace-with-your-token",
)
```

## Configuration

| Argument | Meaning |
| --- | --- |
| `base_url` | InvenioRDM instance root URL |
| `token` | Authentication token (`AuthenticatedClient` only) |
| `prefix` | Authentication prefix; defaults to `Bearer` |
| `auth_header_name` | Authentication header; defaults to `Authorization` |
| `headers` | Headers shared by all requests |
| `cookies` | Cookies shared by all requests |
| `timeout` | `httpx.Timeout` configuration |
| `verify_ssl` | Boolean, CA bundle path, or `ssl.SSLContext` |
| `follow_redirects` | Whether HTTP redirects are followed |
| `raise_on_unexpected_status` | Raise for statuses absent from the contract |
| `httpx_args` | Additional `httpx.Client`/`AsyncClient` constructor arguments |

## Context managers

```python
with client:
    ...
```

```python
async with client:
    ...
```

Context managers close the underlying `httpx` transport on exit.

## Customize the transport

```python
import httpx

client = AuthenticatedClient(
    base_url="https://invenio.example.org",
    token="replace-with-your-token",
    timeout=httpx.Timeout(30),
    httpx_args={
        "limits": httpx.Limits(
            max_connections=20,
            max_keepalive_connections=10,
        )
    },
)
```

Use `set_httpx_client` or `set_async_httpx_client` to supply a completely
configured transport. Doing so overrides construction from the client's stored
connection settings.

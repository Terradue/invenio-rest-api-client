# How to authenticate

Use `AuthenticatedClient` for Record APIs that require an InvenioRDM Bearer
token.

## Provide credentials through the environment

```console
export INVENIO_BASE_URL="https://invenio.example.org"
export INVENIO_TOKEN="replace-with-your-token"
```

```python
import os

from invenio_rest_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    raise_on_unexpected_status=True,
)
```

The client sends:

```http
Authorization: Bearer replace-with-your-token
```

Do not commit tokens to source control or include them in logs.

## Use a custom authentication header

If an API gateway expects another header or an unprefixed token:

```python
client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    prefix="",
    auth_header_name="X-Api-Key",
)
```

## Use a private certificate authority

Pass the path to a CA bundle:

```python
client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    verify_ssl="/path/to/ca-bundle.pem",
)
```

Avoid `verify_ssl=False` outside disposable local development environments; it
disables server identity verification.

## Reuse and close connections

Use the client as a context manager:

```python
from invenio_rest_api_client.api.records import search_records

with client:
    result = search_records.sync(client=client, q="climate")
```

For async code:

```python
from invenio_rest_api_client.api.records import search_records

async with client:
    result = await search_records.asyncio(client=client, q="climate")
```

See [Client reference](../reference/client.md) for configuration options.

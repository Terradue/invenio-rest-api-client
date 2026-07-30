# How to search and retrieve records

Use `search_records` for a result page and `get_a_record_by_id` for one known
record.

## Search records

```python
from invenio_rest_api_client.api.records import search_records

with client:
    result = search_records.sync(
        client=client,
        q='metadata.title:"climate"',
        sort="newest",
        size="25",
        page="1",
    )

if result is None:
    raise RuntimeError("Invenio did not return a search result")

hits = result.get("hits", {}).get("hits", [])
for record in hits:
    print(record["id"], record["metadata"]["title"])
```

The query uses the query syntax supported by the target InvenioRDM instance.
The generated method accepts `size` and `page` as strings because that is how
they are declared in the enhanced OpenAPI contract.

## Include all versions

```python
result = search_records.sync(
    client=client,
    q="climate",
    allversions="true",
)
```

## Retrieve a record by ID

```python
from invenio_rest_api_client.api.records import get_a_record_by_id

record = get_a_record_by_id.sync(
    "abcde-12345",
    client=client,
)
if record is None:
    raise RuntimeError("Record not found or response could not be parsed")

print(record["metadata"]["title"])
```

## Distinguish HTTP failures

Use `sync_detailed` when `None` does not provide enough information:

```python
from http import HTTPStatus

response = get_a_record_by_id.sync_detailed(
    "abcde-12345",
    client=client,
)

if response.status_code is HTTPStatus.OK:
    record = response.parsed
elif response.status_code is HTTPStatus.NOT_FOUND:
    record = None
else:
    raise RuntimeError(
        f"Request failed with {response.status_code}: "
        f"{response.content.decode(errors='replace')}"
    )
```

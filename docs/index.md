# Invenio REST API Client

Use InvenioRDM from Python through a generated client backed by reconstructed
OpenAPI schemas.

This project concentrates on the lifecycle of a record: discovering published
records, creating and updating drafts, managing files, publishing records, and
working with versions.

## Choose what you need

| If you want to… | Go to… |
| --- | --- |
| learn the client by completing a record workflow | [Create your first record](tutorials/first-record.md) |
| accomplish a specific task | [How-to guides](how-to/authenticate.md) |
| look up modules, functions, and return behavior | [Record API reference](reference/records.md) |
| understand why the schemas and client were created | [Schema reconstruction](explanation/schema-reconstruction.md) |

## The short version

The [upstream Invenio OpenAPI documentation](https://inveniosoftware.github.io/invenio-openapi/)
described the REST operations, but at the time this project was developed its
responses did not include the schemas needed for typed client generation.
The missing schemas were reconstructed from the
[human-readable InvenioRDM REST documentation](https://inveniordm.docs.cern.ch/reference/rest_api_drafts_records/),
implemented in the OpenAPI contract, and then used to generate the Python
client and Pydantic models.

## Install

```console
pip install invenio-rest-api-client
```

```python
import os

from invenio_rest_api_client import AuthenticatedClient
from invenio_rest_api_client.api.records import search_records

client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    raise_on_unexpected_status=True,
)

with client:
    records = search_records.sync(
        client=client,
        q='metadata.title:"climate"',
        size="10",
    )
```

For the complete workflow, continue with
[Create your first record](tutorials/first-record.md).

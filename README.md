# Invenio REST API Client

[![PyPI - Version](https://img.shields.io/pypi/v/invenio-rest-api-client.svg)](https://pypi.org/project/invenio-rest-api-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/invenio-rest-api-client.svg)](https://pypi.org/project/invenio-rest-api-client)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A typed Python client for the InvenioRDM REST API, with particular emphasis on
the lifecycle of records and drafts.

## Why this project exists

The [original Invenio OpenAPI description](https://inveniosoftware.github.io/invenio-openapi/)
documented the available operations, but at the time this client was developed
it did not provide the response schemas required to generate a useful typed
client.

This project therefore follows a schema-first reconstruction workflow:

1. study the [human-readable InvenioRDM REST API documentation](https://inveniordm.docs.cern.ch/reference/rest_api_drafts_records/);
2. reconstruct the missing data and response schemas from the documented
   fields and examples;
3. add those schemas to the OpenAPI description;
4. generate Pydantic models and a Python client from the enhanced contract.

Most examples and validation work focus on operations associated with the
OpenAPI `Records` tag and the related draft, file, and version endpoints.

## Install

```console
pip install invenio-rest-api-client
```

Python 3.10 or newer is required.

## Configure a client

Create an API token in your InvenioRDM account and expose the instance URL and
token as environment variables:

```console
export INVENIO_BASE_URL="https://invenio.example.org"
export INVENIO_TOKEN="replace-with-your-token"
```

Then create an authenticated client:

```python
import os

from invenio_rest_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    raise_on_unexpected_status=True,
)
```

## Search and retrieve records

Every endpoint module provides `sync`, `sync_detailed`, `asyncio`, and
`asyncio_detailed` functions.

```python
from invenio_rest_api_client.api.records import (
    get_a_record_by_id,
    search_records,
)

with client:
    results = search_records.sync(
        client=client,
        q='metadata.title:"climate"',
        size="10",
        page="1",
    )

    record = get_a_record_by_id.sync(
        "abcde-12345",
        client=client,
    )
```

Use the detailed form when status codes, headers, or raw response content
matter:

```python
from http import HTTPStatus

from invenio_rest_api_client.api.records import get_a_record_by_id

with client:
    response = get_a_record_by_id.sync_detailed(
        "abcde-12345",
        client=client,
    )

if response.status_code is HTTPStatus.OK:
    record = response.parsed
else:
    raise RuntimeError(
        f"Invenio returned {response.status_code}: "
        f"{response.content.decode(errors='replace')}"
    )
```

## Create and publish a record

The generated request models make the minimum record metadata explicit:

```python
from datetime import date

from invenio_rest_api_client.api.drafts import publish_a_draft_record
from invenio_rest_api_client.api.records import create_a_draft_record
from invenio_rest_api_client.models import (
    Access,
    AccessFiles,
    AccessRecord,
    CreateADraftRecordBody,
    Creator,
    Files,
    Metadata,
    PersonOrOrg,
    PersonOrOrgType,
    ResourceType,
    ResourceTypeId,
)

body = CreateADraftRecordBody(
    access=Access(
        record=AccessRecord.PUBLIC,
        files=AccessFiles.PUBLIC,
    ),
    files=Files(enabled=False),
    metadata=Metadata(
        resource_type=ResourceType(id=ResourceTypeId.DATASET),
        title="Climate observations",
        publication_date=date.today(),
        creators=[
            Creator(
                person_or_org=PersonOrOrg(
                    type=PersonOrOrgType.PERSONAL,
                    given_name="Ada",
                    family_name="Lovelace",
                )
            )
        ],
        publisher="Example Repository",
    ),
)

with client:
    draft = create_a_draft_record.sync(client=client, body=body)
    if draft is None or draft.id is None:
        raise RuntimeError("Invenio did not return the created draft")

    published = publish_a_draft_record.sync(draft.id, client=client)
    if published is None:
        raise RuntimeError("Invenio did not return the published record")
```

## Async usage

The async API mirrors the synchronous API:

```python
from invenio_rest_api_client.api.records import get_a_record_by_id

async with client:
    record = await get_a_record_by_id.asyncio(
        "abcde-12345",
        client=client,
    )
```

## Documentation

The documentation follows the [Diátaxis](https://diataxis.fr/) convention:

- [Tutorial: create your first record](https://terradue.github.io/invenio-rest-api-client/tutorials/first-record/)
- [How-to guides](https://terradue.github.io/invenio-rest-api-client/how-to/authenticate/)
- [Record API reference](https://terradue.github.io/invenio-rest-api-client/reference/records/)
- [Why the schemas were reconstructed](https://terradue.github.io/invenio-rest-api-client/explanation/schema-reconstruction/)
- [Enhanced OpenAPI reference](https://terradue.github.io/invenio-rest-api-client/openapi/invenio.html)

## Development

Run the test and quality suite with:

```console
task quality:pre-commit:run
```

Build the documentation locally with:

```console
mkdocs build --strict
```

## License

Licensed under the [Apache License 2.0](LICENSE).

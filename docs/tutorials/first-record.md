# Tutorial: create your first record

In this tutorial you will create a minimal InvenioRDM draft, inspect the
generated response, and publish it as a record.

The goal is to experience the complete client workflow. For task-oriented
variations, use the [how-to guides](../how-to/create-and-publish.md).

## Prerequisites

You need:

- Python 3.10 or newer;
- access to an InvenioRDM instance;
- an API token created in that instance;
- permission to create records.

The official InvenioRDM documentation describes Bearer tokens as the supported
authentication mechanism for REST API calls.

## 1. Create a project

```console
mkdir invenio-record-example
cd invenio-record-example
python -m venv .venv
source .venv/bin/activate
pip install invenio-rest-api-client
```

## 2. Configure the connection

Keep credentials outside the Python source:

```console
export INVENIO_BASE_URL="https://invenio.example.org"
export INVENIO_TOKEN="replace-with-your-token"
```

Create `create_record.py`:

```python
import os

from invenio_rest_api_client import AuthenticatedClient

client = AuthenticatedClient(
    base_url=os.environ["INVENIO_BASE_URL"],
    token=os.environ["INVENIO_TOKEN"],
    raise_on_unexpected_status=True,
)
```

`raise_on_unexpected_status=True` turns undocumented HTTP statuses into
`UnexpectedStatus` exceptions instead of silently returning `None`.

## 3. Describe the record

Add the imports and request model:

```python
from datetime import date

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
```

The schema makes the minimum metadata visible in Python: resource type, title,
publication date, at least one creator, and publisher.

## 4. Create, publish, and retrieve the record

Add:

```python
from http import HTTPStatus

from invenio_rest_api_client.api.drafts import publish_a_draft_record
from invenio_rest_api_client.api.records import (
    create_a_draft_record,
    get_a_record_by_id,
)

with client:
    response = create_a_draft_record.sync_detailed(
        client=client,
        body=body,
    )

    if response.status_code is not HTTPStatus.CREATED:
        raise RuntimeError(
            f"Could not create draft ({response.status_code}): "
            f"{response.content.decode(errors='replace')}"
        )

    draft = response.parsed
    if draft is None or draft.id is None:
        raise RuntimeError("The create response did not contain a draft ID")

    print(f"Created draft {draft.id}")

    published = publish_a_draft_record.sync(
        draft.id,
        client=client,
    )
    if published is None or published.id is None:
        raise RuntimeError("The publish response did not contain a record ID")

    print(f"Published record {published.id}")

    record = get_a_record_by_id.sync(
        published.id,
        client=client,
    )
    if record is None:
        raise RuntimeError("The published record could not be retrieved")

    print(record["metadata"]["title"])
```

The `sync_detailed` function is useful here because it preserves the status,
headers, raw body, and parsed model in one `Response` object.

## 5. Run the workflow

Run the script:

```console
python create_record.py
```

You should see the draft identifier followed by the published record
identifier.

The last line should be:

```text
Climate observations
```

## What you learned

You have:

- configured an authenticated client;
- built a validated record request with Pydantic models;
- used a detailed response for explicit HTTP handling;
- created a draft and published it;
- retrieved the resulting record.

Next, learn how to [search records](../how-to/search-records.md) or read the
[Record API reference](../reference/records.md).

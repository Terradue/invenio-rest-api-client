# How to create and publish a record

Create a draft with the `Records` API and publish it with the related `Drafts`
API.

## Build a minimal request

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

## Create the draft

```python
from invenio_rest_api_client.api.records import create_a_draft_record

draft = create_a_draft_record.sync(client=client, body=body)
if draft is None or draft.id is None:
    raise RuntimeError("Invenio did not return the created draft")
```

## Publish it

```python
from invenio_rest_api_client.api.drafts import publish_a_draft_record

published = publish_a_draft_record.sync(
    draft.id,
    client=client,
)
if published is None:
    raise RuntimeError("Invenio did not return the published record")
```

## Keep a draft unpublished

Stop after draft creation when the record needs review, file uploads, DOI
reservation, or further metadata changes. Relevant modules include:

- `api.drafts.update_a_draft_record`;
- `api.drafts.reserve_a_doi`;
- `api.drafts_files_upload.step_1_start_draft_file_uploads`;
- `api.drafts_files_upload.step_2_upload_a_draft_files_content`;
- `api.drafts_files_upload.step_3_complete_a_draft_file_upload`.

See [Record API reference](../reference/records.md) for the complete map.

# Record API reference

The generated client maps each OpenAPI operation to a Python module. Record
lifecycle operations are split across several OpenAPI tags, so their modules
live in related packages.

## Function variants

Every generated endpoint exposes four functions:

| Function | I/O model | Return value |
| --- | --- | --- |
| `sync` | blocking | parsed model/data or `None` |
| `sync_detailed` | blocking | `Response` with status, headers, content, and parsed data |
| `asyncio` | async | parsed model/data or `None` |
| `asyncio_detailed` | async | `Response` with status, headers, content, and parsed data |

When `raise_on_unexpected_status=True`, a status not declared by the OpenAPI
operation raises `UnexpectedStatus`.

## Records

Import from `invenio_rest_api_client.api.records`.

| Module | Purpose |
| --- | --- |
| `search_records` | Search published records |
| `get_a_record_by_id` | Retrieve one published record |
| `create_a_draft_record` | Begin a new record as a draft |
| `delete_record_community` | Remove a record from a community |
| `create_an_access_link` | Create a secret access link |
| `get_an_access_link_by_id` | Retrieve an access link |
| `list_access_links` | List a record's access links |
| `update_an_access_link` | Update an access link |
| `delete_an_access_link` | Delete an access link |

## Drafts

Import from `invenio_rest_api_client.api.drafts`.

| Module | Purpose |
| --- | --- |
| `get_a_draft_records` | Retrieve a draft |
| `update_a_draft_record` | Replace draft metadata/options |
| `deletediscard_a_draft_record` | Discard a draft |
| `publish_a_draft_record` | Publish a draft as a record |
| `edit_a_published_record_create_a_draft_record_from_a_published_record` | Create an editable draft from a published record |
| `reserve_a_doi` | Reserve a DOI |
| `delete_a_doi` | Remove a reserved DOI |
| `submit_a_record_for_review` | Submit a draft for review |
| `get_a_review_request` | Retrieve its review request |
| `createupdate_a_review_request` | Create or update its review request |
| `delete_a_review_request` | Delete its review request |
| `link_files_from_previous_version` | Link files from the previous version |

## Draft file upload

Import from `invenio_rest_api_client.api.drafts_files_upload`.

| Module | Purpose |
| --- | --- |
| `step_1_start_draft_file_uploads` | Initialize one or more file uploads |
| `step_2_upload_a_draft_files_content` | Upload raw file content |
| `step_3_complete_a_draft_file_upload` | Commit an uploaded file |

Draft file metadata and deletion operations are available under
`invenio_rest_api_client.api.drafts`.

## Published record files

Import from `invenio_rest_api_client.api.records_files`.

| Module | Purpose |
| --- | --- |
| `list_a_records_files` | List files attached to a record |
| `get_a_record_files_metadata` | Retrieve metadata for one file |
| `download_a_record_file` | Download file content |

## Record versions

Import from `invenio_rest_api_client.api.records_versions`.

| Module | Purpose |
| --- | --- |
| `get_all_versions` | List all versions |
| `get_latest_version` | Retrieve the latest version |
| `create_a_new_version` | Start a new draft version |

## Common types

`invenio_rest_api_client.models` contains the generated Pydantic request and
response models. Important Record models include:

- `CreateADraftRecordBody`;
- `UpdateDraftRecord`;
- `Metadata`;
- `Creator` and `PersonOrOrg`;
- `Access` and `Files`;
- `Created`.

`invenio_rest_api_client.types.Response[T]` contains:

- `status_code`;
- raw `content`;
- response `headers`;
- optional `parsed` data.

For the complete HTTP contract, use the
[enhanced OpenAPI reference](../openapi/invenio.html).

# InvenioRDM v12.0.3 OpenAPI audit — Records/Drafts and Zenodo compatibility

## Scope

This audit compares `Terradue/invenio-rest-api-client` tag `v12.0.3` against:

- the current public `inveniosoftware/invenio-openapi` specification;
- the actual InvenioRDM v12.0.3 service/resource schemas (`invenio-rdm-records` plus its v5/v6 draft/record resource dependencies);
- Zenodo's current `zenodo-rdm` record serializer override.

The supplied patch focuses on the Records/Drafts contract because that is where strict generated models currently fail. The remaining API groups still contain generic `Success`/`Created` response definitions and should be audited endpoint-by-endpoint before making them strongly typed.

## High-confidence corrections included in the patch

| Area | Existing declaration | Runtime/source behavior | Patch |
|---|---|---|---|
| Shared `Created` response | Forced every `201` through a record-shaped `Created` model | `Created` is used by unrelated endpoints | Restore generic response; add record-specific responses |
| `POST /api/records` | `201 -> Created` | Returns a record/draft item | `201 -> RecordCreated -> RecordResponse` |
| Zenodo `application/json` | Assumed canonical Invenio record | Zenodo deliberately replaces the default record serializer with `ZenodoJSONSerializer` | `RecordResponse = oneOf[RDMRecord, ZenodoRecord]` |
| Zenodo `id` | string | integer | `ZenodoRecord.id: integer` |
| Zenodo `files` | `Files` object | array | `ZenodoRecord.files: array[ZenodoFile]` |
| Canonical files | Only input options modeled | v12 `FilesSchema` also emits `count`, `total_bytes`, `entries` | Add read-only output properties |
| PID | typo `type": string`; no required fields | `identifier` and `provider` are required | Fix typo and requirements |
| Draft metadata | Full publish-time required fields | drafts are saved with validation errors (`raise_errors=False`) | Remove `Metadata.required` for draft/general representation |
| `publisher` | required | optional in v12 `MetadataSchema` | no longer required |
| publication/date fields | `format: date` | EDTF strings, including intervals/partial dates | remove `format: date` |
| contributors | reused `Creator`, role optional | contributor role required | add `Contributor` schema |
| locations | array of container objects | object containing `features` array | reference the existing location container directly |
| rights | `links` URI | v12 has `props`, singular `link`, and dump-only `icon` | correct properties |
| vocabulary relation labels | `title` required | relation input needs ID; display title is output enrichment | make title read-only/non-required |
| draft update example | `enabled: "false"` | boolean | `enabled: false` |
| publish status | `201` | v5 draft resource returns `202` | `202 -> RecordAccepted` |
| delete draft status | `200` | v5 draft resource returns `204` | `204 -> NoContent` |
| latest-version endpoint | `200` | raises redirect with HTTP `301` + `Location` | model `301` redirect |

## Important issues intentionally not guessed in this patch

### Search/list responses

`GET /api/records`, `GET /api/user/records`, and versions searches still use the generic `Success` response. Runtime responses are search-result envelopes and should get dedicated list/search schemas rather than being inferred from a single payload.

### File endpoints

File initialization, commit, metadata, and content endpoints use response shapes distinct from records. The old global record-shaped `Created` was especially dangerous here. The patch restores generic handling but does not invent detailed file-operation responses without tracing each resource method.

### Export/content media types

Several export and content-download endpoints still reuse a JSON `Success` response even when the real payload is XML, BibTeX, binary content, etc. These should be corrected with operation-specific `content` media types.

### Controlled-vocabulary enums

The hand-written specification turns multiple configurable vocabulary IDs into Python enums (resource type, roles, identifier schemes, relation types, etc.). This is convenient for a stock instance but too strict for a generic InvenioRDM client because several vocabularies/schemes are deployment-configurable. A second hardening pass should replace configurable enums with strings plus examples/descriptions, while keeping genuinely fixed enums such as person/organization type and access protection values.

### Missing/under-described routes

The runtime record resource exposes more route semantics than the manual public specification captures. A complete API-wide contract should be generated from configured runtime resources where possible rather than continuing to treat the public manual YAML as authoritative.

## Recommended source-of-truth strategy

1. Use the public `inveniosoftware/invenio-openapi` only as a route/documentation baseline.
2. Ground strongly typed schemas and status codes in the tagged implementation corresponding to the intended InvenioRDM version.
3. Treat Zenodo as a deployment profile: it intentionally changes the JSON record representation.
4. Keep operation-specific response components (`RecordCreated`, `RecordSuccess`, etc.) rather than a universal typed `Created`/`Success`.
5. Add captured runtime payloads as regression tests before regenerating the Python client.

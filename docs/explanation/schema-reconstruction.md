# Why the schemas were reconstructed

This client exists because an API operation list alone is not enough to
generate a useful typed SDK.

## The original gap

The [original Invenio OpenAPI site](https://inveniosoftware.github.io/invenio-openapi/)
provided a machine-readable catalogue of InvenioRDM endpoints. At the time this
work began, however, response payloads did not provide the schemas needed to
describe their data shapes.

That omission matters to a generator. Without a response schema it can produce
an HTTP call, but it cannot reliably determine:

- which Python model to return;
- which fields are required or optional;
- which nested objects and enumerations exist;
- how dates, identifiers, access settings, and record metadata should be
  validated;
- whether a change in the response contract is compatible.

The generated result would therefore be dominated by unstructured dictionaries
or `Any`, losing much of the value of a typed client.

## The human-readable source

The missing semantics were available in the
[InvenioRDM Drafts and Records reference](https://inveniordm.docs.cern.ch/reference/rest_api_drafts_records/).
Its prose, field tables, and JSON examples explain real payloads for operations
such as:

- creating a draft;
- uploading and committing files;
- publishing a draft;
- retrieving records;
- managing access links and versions.

Those documents are designed for people, not code generators. The work in this
repository translates that human-readable contract into machine-readable
schemas.

## The reconstruction pipeline

```text
Human-readable InvenioRDM documentation
                  |
                  v
Reconstructed request, metadata, and response schemas
                  |
                  v
Enhanced OpenAPI contract
                  |
          +-------+-------+
          |               |
          v               v
Generated API modules   Pydantic models
          |               |
          +-------+-------+
                  |
                  v
        Typed Python client
```

The practical sequence is:

1. identify the payload fields and constraints in the textual documentation;
2. model reusable concepts such as `Metadata`, `Creator`, `Access`, `Files`,
   persistent identifiers, and the created record response;
3. connect those schemas to requests and responses in the OpenAPI document;
4. bundle and validate the enhanced contract;
5. generate endpoint modules and Pydantic models;
6. exercise the generated behavior with contract and unit tests.

## Why focus on Records

Records are the central resource in InvenioRDM and touch multiple stages:

```text
search/get -> create draft -> edit/upload/review -> publish -> version
```

Although the OpenAPI description separates these operations into tags such as
`Records`, `Drafts`, `Drafts Files upload`, `Records Files`, and
`Records Versions`, they form one user-facing lifecycle. That lifecycle is the
main showcase and validation target for this client.

## What this approach provides

The enhanced contract enables:

- discoverable Python request models;
- validation before a request is sent;
- parsed Pydantic responses where a concrete schema is linked;
- consistent synchronous and asynchronous functions;
- generated documentation and a browsable OpenAPI reference;
- tests that can detect drift across every generated endpoint.

Schema reconstruction is still an interpretation of upstream documentation.
When InvenioRDM changes, both the enhanced OpenAPI contract and the generated
client should be regenerated and verified against the target server version.

# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Regression tests for InvenioRDM and Zenodo record representations."""

from http import HTTPStatus
from typing import Any

import httpx

from invenio_rest_api_client import Client
from invenio_rest_api_client.api.records import create_a_draft_record


def _created_response(payload: dict[str, Any]) -> httpx.Response:
    request = httpx.Request("POST", "https://example.test/api/records")
    return httpx.Response(HTTPStatus.CREATED, json=payload, request=request)


def test_create_draft_parses_canonical_invenio_record() -> None:
    payload = {
        "id": "abcde-12345",
        "created": "2026-08-27T10:35:36.996497+00:00",
        "updated": "2026-08-27T10:35:37.108289+00:00",
        "revision_id": 1,
        "is_published": False,
        "is_draft": True,
        "metadata": {},
        "files": {
            "enabled": True,
            "count": 0,
            "total_bytes": 0,
            "entries": {},
        },
    }

    parsed = create_a_draft_record._parse_response(
        client=Client(base_url="https://example.test"),
        response=_created_response(payload),
    )

    assert parsed is not None
    assert parsed.model_dump(mode="json")["id"] == "abcde-12345"


def test_create_draft_parses_zenodo_record() -> None:
    payload = {
        "created": "2026-08-27T10:35:36.996497+00:00",
        "modified": "2026-08-27T10:35:37.108289+00:00",
        "id": 593097,
        "conceptrecid": "593096",
        "metadata": {
            "access_right": "open",
            "relations": {
                "version": [
                    {
                        "index": 0,
                        "is_last": False,
                        "parent": {"pid_type": "recid", "pid_value": "593096"},
                    }
                ]
            },
        },
        "title": "",
        "links": {
            "self": "https://sandbox.zenodo.org/api/records/593097/draft",
            "files": "https://sandbox.zenodo.org/api/records/593097/draft/files",
        },
        "updated": "2026-08-27T10:35:37.108289+00:00",
        "recid": "593097",
        "revision": 4,
        "files": [],
        "owners": [{"id": "48746"}],
        "status": "draft",
        "state": "unsubmitted",
        "submitted": False,
    }

    parsed = create_a_draft_record._parse_response(
        client=Client(base_url="https://example.test"),
        response=_created_response(payload),
    )

    assert parsed is not None
    data = parsed.model_dump(mode="json")
    assert data["id"] == 593097
    assert data["files"] == []

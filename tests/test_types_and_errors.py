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

"""Tests for shared response, upload, and error types."""

from http import HTTPStatus
from io import BytesIO

from invenio_rest_api_client.errors import UnexpectedStatus
from invenio_rest_api_client.types import UNSET, File, Response, Unset


def test_unset_is_always_falsy() -> None:
    assert not UNSET
    assert not Unset()


def test_file_converts_to_httpx_upload_tuple() -> None:
    payload = BytesIO(b"content")
    upload = File(payload=payload, file_name="data.txt", mime_type="text/plain")

    assert upload.to_tuple() == ("data.txt", payload, "text/plain")


def test_response_keeps_transport_and_parsed_values() -> None:
    response = Response(
        status_code=HTTPStatus.OK,
        content=b'{"ok": true}',
        headers={"X-Request-ID": "123"},
        parsed={"ok": True},
    )

    assert response.status_code is HTTPStatus.OK
    assert response.content == b'{"ok": true}'
    assert response.headers["X-Request-ID"] == "123"
    assert response.parsed == {"ok": True}


def test_unexpected_status_includes_code_and_safe_content() -> None:
    error = UnexpectedStatus(418, b"invalid: \xff")

    assert error.status_code == 418
    assert error.content == b"invalid: \xff"
    assert "Unexpected status code: 418" in str(error)
    assert "invalid:" in str(error)

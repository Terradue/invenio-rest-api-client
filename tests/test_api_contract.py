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

"""Contract tests shared by every generated API endpoint."""

import asyncio
import importlib
import inspect
import pkgutil
from http import HTTPStatus
from io import BytesIO
from typing import Any, Protocol, cast, get_origin

import httpx
import pytest
from pydantic import BaseModel

from invenio_rest_api_client import AuthenticatedClient, Client, api
from invenio_rest_api_client.api.audit_logs import retrieve_log_entry
from invenio_rest_api_client.errors import UnexpectedStatus
from invenio_rest_api_client.models import AuditLogEntry
from invenio_rest_api_client.types import File, Response


class EndpointModule(Protocol):
    """The common call surface emitted for every generated endpoint."""

    __name__: str

    def _get_kwargs(self, **kwargs: Any) -> dict[str, Any]: ...

    def _parse_response(
        self, *, client: AuthenticatedClient | Client, response: httpx.Response
    ) -> Any: ...

    def sync_detailed(
        self, *, client: AuthenticatedClient, **kwargs: Any
    ) -> Response[Any]: ...

    def sync(self, *, client: AuthenticatedClient, **kwargs: Any) -> Any: ...

    async def asyncio_detailed(
        self, *, client: AuthenticatedClient, **kwargs: Any
    ) -> Response[Any]: ...

    async def asyncio(self, *, client: AuthenticatedClient, **kwargs: Any) -> Any: ...


def _endpoint_modules() -> list[EndpointModule]:
    modules: list[EndpointModule] = []
    for module_info in pkgutil.walk_packages(api.__path__, f"{api.__name__}."):
        if not module_info.ispkg:
            module = importlib.import_module(module_info.name)
            modules.append(cast("EndpointModule", module))
    return modules


ENDPOINT_MODULES = _endpoint_modules()


def _required_arguments(module: EndpointModule) -> dict[str, Any]:
    arguments: dict[str, Any] = {}
    signature = inspect.signature(module._get_kwargs)
    for parameter in signature.parameters.values():
        if parameter.default is not inspect.Parameter.empty:
            continue

        annotation = parameter.annotation
        if parameter.name != "body":
            arguments[parameter.name] = "value / with spaces"
        elif annotation is File:
            arguments[parameter.name] = File(BytesIO(b"content"))
        elif get_origin(annotation) is dict:
            arguments[parameter.name] = {}
        elif get_origin(annotation) is list:
            arguments[parameter.name] = []
        elif isinstance(annotation, type) and issubclass(annotation, BaseModel):
            arguments[parameter.name] = annotation.model_construct()
        else:
            raise AssertionError(
                f"Unsupported required argument {parameter.name}: {annotation!r}"
            )
    return arguments


def _bad_request(_: httpx.Request) -> httpx.Response:
    return httpx.Response(HTTPStatus.BAD_REQUEST, content=b"bad request")


@pytest.mark.parametrize(
    "module",
    ENDPOINT_MODULES,
    ids=lambda module: module.__name__.removeprefix("invenio_rest_api_client.api."),
)
def test_generated_endpoint_transport_contract(module: EndpointModule) -> None:
    kwargs = module._get_kwargs(**_required_arguments(module))
    assert kwargs["method"] in {"delete", "get", "patch", "post", "put"}
    assert cast("str", kwargs["url"]).startswith("/api/")

    sync_client = AuthenticatedClient(
        base_url="https://example.test",
        token="secret",
        httpx_args={"transport": httpx.MockTransport(_bad_request)},
    )
    detailed = module.sync_detailed(client=sync_client, **_required_arguments(module))
    assert detailed.status_code is HTTPStatus.BAD_REQUEST
    assert detailed.content == b"bad request"
    assert detailed.parsed is None
    assert module.sync(client=sync_client, **_required_arguments(module)) is None
    sync_client.get_httpx_client().close()

    async def exercise_async() -> None:
        async_client = AuthenticatedClient(
            base_url="https://example.test",
            token="secret",
            httpx_args={"transport": httpx.MockTransport(_bad_request)},
        )
        detailed_async = await module.asyncio_detailed(
            client=async_client, **_required_arguments(module)
        )
        assert detailed_async.status_code is HTTPStatus.BAD_REQUEST
        assert detailed_async.parsed is None
        assert (
            await module.asyncio(client=async_client, **_required_arguments(module))
            is None
        )
        await async_client.get_async_httpx_client().aclose()

    if not {"content", "files"} & kwargs.keys():
        asyncio.run(exercise_async())


def _response(status: int, *, json: Any = None, content: bytes = b"") -> httpx.Response:
    request = httpx.Request("GET", "https://example.test")
    if json is not None:
        return httpx.Response(status, json=json, request=request)
    return httpx.Response(status, content=content, request=request)


def test_retrieve_log_entry_quotes_paths_and_parses_success() -> None:
    assert retrieve_log_entry._get_kwargs("log / one") == {
        "method": "get",
        "url": "/api/audit-logs/log%20%2F%20one",
    }
    parsed = retrieve_log_entry._parse_response(
        client=Client(base_url="https://example.test"),
        response=_response(200, json={"id": "entry-1", "action": "record.publish"}),
    )

    assert isinstance(parsed, AuditLogEntry)
    assert parsed.id == "entry-1"
    assert parsed.action == "record.publish"


@pytest.mark.parametrize("status", [400, 401, 403, 404, 500])
def test_retrieve_log_entry_handles_documented_empty_errors(status: int) -> None:
    parsed = retrieve_log_entry._parse_response(
        client=Client(base_url="https://example.test"),
        response=_response(status),
    )

    assert parsed is None


def test_retrieve_log_entry_controls_unexpected_status_handling() -> None:
    response = _response(418, content=b"teapot")
    assert (
        retrieve_log_entry._parse_response(
            client=Client(base_url="https://example.test"),
            response=response,
        )
        is None
    )

    strict_client = Client(
        base_url="https://example.test", raise_on_unexpected_status=True
    )
    with pytest.raises(UnexpectedStatus, match="418"):
        retrieve_log_entry._parse_response(client=strict_client, response=response)

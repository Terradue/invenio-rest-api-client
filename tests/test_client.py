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

"""Tests for synchronous and asynchronous client configuration."""

import asyncio

import httpx

from invenio_rest_api_client import AuthenticatedClient, Client


def _ok_response(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"url": str(request.url)})


def test_client_builds_and_reuses_sync_transport() -> None:
    transport = httpx.MockTransport(_ok_response)
    client = Client(
        base_url="https://example.test/api",
        headers={"X-Test": "initial"},
        cookies={"session": "cookie"},
        follow_redirects=True,
        httpx_args={"transport": transport},
    )

    http_client = client.get_httpx_client()

    assert client.get_httpx_client() is http_client
    assert http_client.follow_redirects is True
    response = http_client.get("/resource")
    assert response.json() == {"url": "https://example.test/api/resource"}
    assert response.request.headers["X-Test"] == "initial"
    assert response.request.headers["Cookie"] == "session=cookie"
    http_client.close()


def test_client_evolution_updates_existing_transports() -> None:
    transport = httpx.MockTransport(_ok_response)
    client = Client(
        base_url="https://example.test",
        httpx_args={"transport": transport},
    )
    sync_client = client.get_httpx_client()
    async_client = client.get_async_httpx_client()
    timeout = httpx.Timeout(3)

    with_headers = client.with_headers({"X-Added": "yes"})
    with_cookies = client.with_cookies({"flavour": "chocolate"})
    with_timeout = client.with_timeout(timeout)

    assert sync_client.headers["X-Added"] == "yes"
    assert async_client.headers["X-Added"] == "yes"
    assert sync_client.cookies["flavour"] == "chocolate"
    assert async_client.cookies["flavour"] == "chocolate"
    assert sync_client.timeout == timeout
    assert async_client.timeout == timeout
    assert with_headers.get_httpx_client().headers["X-Added"] == "yes"
    assert with_cookies.get_httpx_client().cookies["flavour"] == "chocolate"
    assert with_timeout.get_httpx_client().timeout == timeout

    sync_client.close()
    with_headers.get_httpx_client().close()
    with_cookies.get_httpx_client().close()
    with_timeout.get_httpx_client().close()
    asyncio.run(async_client.aclose())


def test_sync_context_manager_and_manually_supplied_client() -> None:
    supplied = httpx.Client(
        base_url="https://example.test",
        transport=httpx.MockTransport(_ok_response),
    )
    client = Client(base_url="https://unused.test").set_httpx_client(supplied)

    with client as entered:
        assert entered is client
        assert entered.get_httpx_client().get("/").status_code == 200

    assert supplied.is_closed


def test_authenticated_client_adds_authorization_headers() -> None:
    transport = httpx.MockTransport(_ok_response)
    client = AuthenticatedClient(
        base_url="https://example.test",
        token="secret",
        httpx_args={"transport": transport},
    )

    response = client.get_httpx_client().get("/")

    assert response.request.headers["Authorization"] == "Bearer secret"
    client.get_httpx_client().close()

    unprefixed = AuthenticatedClient(
        base_url="https://example.test",
        token="raw-token",
        prefix="",
        auth_header_name="X-Api-Key",
        httpx_args={"transport": transport},
    )
    response = unprefixed.get_httpx_client().get("/")
    assert response.request.headers["X-Api-Key"] == "raw-token"
    unprefixed.get_httpx_client().close()


def test_authenticated_client_evolution_updates_existing_transports() -> None:
    transport = httpx.MockTransport(_ok_response)
    client = AuthenticatedClient(
        base_url="https://example.test",
        token="secret",
        httpx_args={"transport": transport},
    )
    sync_client = client.get_httpx_client()
    async_client = client.get_async_httpx_client()
    timeout = httpx.Timeout(2)

    with_headers = client.with_headers({"X-Added": "yes"})
    with_cookies = client.with_cookies({"flavour": "vanilla"})
    with_timeout = client.with_timeout(timeout)

    assert sync_client.headers["X-Added"] == "yes"
    assert async_client.headers["X-Added"] == "yes"
    assert sync_client.cookies["flavour"] == "vanilla"
    assert async_client.cookies["flavour"] == "vanilla"
    assert sync_client.timeout == timeout
    assert async_client.timeout == timeout
    assert with_headers.token == "secret"
    assert with_cookies.token == "secret"
    assert with_timeout.token == "secret"

    sync_client.close()
    asyncio.run(async_client.aclose())


def test_async_context_managers_and_manually_supplied_clients() -> None:
    async def exercise() -> None:
        supplied = httpx.AsyncClient(
            base_url="https://example.test",
            transport=httpx.MockTransport(_ok_response),
        )
        client = Client(base_url="https://unused.test").set_async_httpx_client(supplied)

        async with client as entered:
            assert entered is client
            assert (await entered.get_async_httpx_client().get("/")).status_code == 200

        assert supplied.is_closed

        authenticated = AuthenticatedClient(
            base_url="https://example.test",
            token="async-secret",
            httpx_args={"transport": httpx.MockTransport(_ok_response)},
        )
        async with authenticated:
            response = await authenticated.get_async_httpx_client().get("/")
            assert response.request.headers["Authorization"] == "Bearer async-secret"

    asyncio.run(exercise())

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

# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models import AuditLogList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str | Unset = UNSET,
    size: str | Unset = UNSET,
    page: str | Unset = UNSET,
    sort: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["size"] = size

    params["page"] = page

    params["sort"] = sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/audit-logs",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | AuditLogList | None:
    if response.status_code == 200:
        response_200 = AuditLogList.model_validate(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast("Any", None)
        return response_400

    if response.status_code == 401:
        response_401 = cast("Any", None)
        return response_401

    if response.status_code == 403:
        response_403 = cast("Any", None)
        return response_403

    if response.status_code == 404:
        response_404 = cast("Any", None)
        return response_404

    if response.status_code == 500:
        response_500 = cast("Any", None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | AuditLogList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    size: str | Unset = UNSET,
    page: str | Unset = UNSET,
    sort: str | Unset = UNSET,
) -> Response[Any | AuditLogList]:
    """Search Logs (Admins only)

     Search and filter audit log entries based on various parameters.

    Args:
        q (str | Unset):
        size (str | Unset):
        page (str | Unset):
        sort (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuditLogList]
    """

    kwargs = _get_kwargs(
        q=q,
        size=size,
        page=page,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    size: str | Unset = UNSET,
    page: str | Unset = UNSET,
    sort: str | Unset = UNSET,
) -> Any | AuditLogList | None:
    """Search Logs (Admins only)

     Search and filter audit log entries based on various parameters.

    Args:
        q (str | Unset):
        size (str | Unset):
        page (str | Unset):
        sort (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuditLogList
    """

    return sync_detailed(
        client=client,
        q=q,
        size=size,
        page=page,
        sort=sort,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    size: str | Unset = UNSET,
    page: str | Unset = UNSET,
    sort: str | Unset = UNSET,
) -> Response[Any | AuditLogList]:
    """Search Logs (Admins only)

     Search and filter audit log entries based on various parameters.

    Args:
        q (str | Unset):
        size (str | Unset):
        page (str | Unset):
        sort (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuditLogList]
    """

    kwargs = _get_kwargs(
        q=q,
        size=size,
        page=page,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: str | Unset = UNSET,
    size: str | Unset = UNSET,
    page: str | Unset = UNSET,
    sort: str | Unset = UNSET,
) -> Any | AuditLogList | None:
    """Search Logs (Admins only)

     Search and filter audit log entries based on various parameters.

    Args:
        q (str | Unset):
        size (str | Unset):
        page (str | Unset):
        sort (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuditLogList
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            size=size,
            page=page,
            sort=sort,
        )
    ).parsed

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

"""Smoke tests for the generated client package."""

from invenio_rest_api_client import AuthenticatedClient, Client


def test_public_clients_are_importable() -> None:
    """The package exposes both generated client implementations."""
    assert Client.__name__ == "Client"
    assert AuthenticatedClient.__name__ == "AuthenticatedClient"

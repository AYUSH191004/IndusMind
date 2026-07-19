"""
Health endpoint integration tests.
"""

from __future__ import annotations

from http import HTTPStatus


async def test_health_endpoint(client):
    """
    Verify that the health endpoint is reachable.
    """
    response = await client.get("/health")

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert body["status"] == "healthy"


async def test_root_endpoint(client):
    """
    Verify that the root endpoint is reachable.
    """
    response = await client.get("/")

    assert response.status_code == HTTPStatus.OK

    body = response.json()

    assert "message" in body

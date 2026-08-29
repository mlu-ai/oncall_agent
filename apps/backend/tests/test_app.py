from __future__ import annotations

from fastapi.testclient import TestClient

from super_ai.app import create_app


def test_health_endpoint_returns_healthy_status() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

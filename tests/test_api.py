from fastapi.testclient import TestClient

from app.main import app
from app.sample_data import SAMPLE_ORCHESTRATIONS


client = TestClient(app)


def test_root_returns_service_metadata() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["docs"] == "/docs"


def test_healthcheck_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_orchestration_list_returns_array() -> None:
    response = client.get("/api/orchestrations")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload
    assert "orchestration_id" in payload[0]


def test_analyze_orchestration_returns_score_and_status() -> None:
    response = client.post(
        "/api/analyze/orchestration",
        json=SAMPLE_ORCHESTRATIONS[0].model_dump(),
    )
    assert response.status_code == 200
    payload = response.json()
    assert "score" in payload
    assert "status" in payload
    assert "routed_actions" in payload


def test_analyze_graph_returns_edges() -> None:
    response = client.post("/api/analyze/graph", json=SAMPLE_ORCHESTRATIONS[0].model_dump())
    assert response.status_code == 200
    payload = response.json()
    assert "nodes" in payload
    assert "edges" in payload

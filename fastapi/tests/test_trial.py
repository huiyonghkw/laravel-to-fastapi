"""试读档冒烟测试：只覆盖 EP00 / EP02 / EP05。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_tier():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["tier"] == "oss-trial"
    assert r.json()["free_eps"] == ["ep00", "ep02", "ep05"]


def test_hello():
    r = client.get("/ep00/hello")
    assert r.status_code == 200
    assert r.json()["framework"] == "FastAPI"


def test_route_health():
    r = client.get("/ep02/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_validate_missing_email():
    r = client.post("/ep05/users", json={"name": "a"})
    assert r.status_code == 422


def test_validate_ok_response_model():
    r = client.post(
        "/ep05/users",
        json={"name": "alice", "email": "alice@example.com", "age": 20},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "alice"
    assert "age" not in body

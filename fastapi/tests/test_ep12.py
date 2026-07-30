"""EP12 测试：Pest / PHPUnit vs pytest + TestClient

Laravel：tests/Feature/ 里用 Pest/PHPUnit 断言响应。
FastAPI：TestClient（基于 httpx）对应用发请求，断言状态码/JSON。
运行（在 fastapi/ 目录）：pytest
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    # 对照 Laravel: $this->get('/api/ep00/hello')->assertOk();
    r = client.get("/ep00/hello")
    assert r.status_code == 200
    assert r.json()["framework"] == "FastAPI"


def test_validate_missing_email():
    # 对照 Laravel: $this->post('/users', [])->assertStatus(422);
    r = client.post("/ep05/users", json={"name": "a"})  # 缺 email → 422
    assert r.status_code == 422


def test_validate_ok_response_model():
    r = client.post(
        "/ep05/users",
        json={"name": "alice", "email": "alice@example.com", "age": 20},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["name"] == "alice"
    assert "age" not in body  # response_model=UserOut 不暴露 age


def test_di_nested():
    r = client.get("/ep09/db-url")
    assert r.status_code == 200
    assert r.json()["url"].startswith("db://")


def test_orm_seed_and_list():
    s = client.post("/ep06/seed")
    assert s.status_code == 200
    r = client.get("/ep06/posts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_transaction_rollback():
    before = client.get("/ep08/orders").json()
    bad = client.post("/ep08/orders", json={"amount": 10, "fail": True})
    assert bad.status_code == 400
    after = client.get("/ep08/orders").json()
    assert len(after) == len(before)  # 失败未写入


def test_auth_login_and_me():
    # OAuth2PasswordRequestForm 要 form 编码
    login = client.post(
        "/ep11/login",
        data={"username": "alice", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    me = client.get("/ep11/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["user"] == "alice"


def test_advise_need_ai():
    r = client.post(
        "/ep15/advise",
        json={
            "has_frontend": False,
            "need_realtime": False,
            "team_knows_php": True,
            "need_ai": True,
        },
    )
    assert r.status_code == 200
    assert r.json()["pick"] == "FastAPI"

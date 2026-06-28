import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models.user import User


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(client: TestClient):
    """创建测试用户（普通成员）并返回用户信息"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    return data["data"]


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient, test_user):
    """获取普通成员认证 headers"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    token = data["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="seed_user")
def seed_user_fixture(client: TestClient, session: Session):
    """创建种子成员用户并返回用户信息"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "seeduser",
            "password": "seed123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    # 直接在数据库中升级角色为 seed_member
    user = session.get(User, data["data"]["id"])
    user.role = "seed_member"
    session.add(user)
    session.commit()
    return data["data"]


@pytest.fixture(name="seed_headers")
def seed_headers_fixture(client: TestClient, seed_user):
    """获取种子成员认证 headers"""
    response = client.post(
        "/api/auth/login",
        json={"username": "seeduser", "password": "seed123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    token = data["data"]["token"]
    return {"Authorization": f"Bearer {token}"}

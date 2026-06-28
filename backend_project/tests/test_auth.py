import pytest
from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    """测试用户注册成功"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "注册成功"
    assert data["data"]["username"] == "newuser"


def test_register_duplicate_username(client: TestClient, test_user):
    """测试重复用户名注册失败"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 400
    assert "已被注册" in data["message"]


def test_login_success(client: TestClient, test_user):
    """测试用户登录成功"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "登录成功"
    assert "token" in data["data"]
    assert data["data"]["user"]["username"] == "testuser"


def test_login_wrong_password(client: TestClient, test_user):
    """测试错误密码登录失败"""
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 400
    assert "用户名或密码错误" in data["message"]


def test_login_nonexistent_user(client: TestClient):
    """测试不存在的用户登录失败"""
    response = client.post(
        "/api/auth/login",
        json={"username": "nonexistent", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 400
    assert "用户名或密码错误" in data["message"]


def test_get_profile_success(client: TestClient, auth_headers):
    """测试获取用户信息成功"""
    response = client.get("/api/auth/profile", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["username"] == "testuser"


def test_get_profile_unauthorized(client: TestClient):
    """测试未认证获取用户信息失败"""
    response = client.get("/api/auth/profile")
    assert response.status_code in (401, 403)  # 权限系统返回 401 或 403

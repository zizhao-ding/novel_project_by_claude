import pytest
from fastapi.testclient import TestClient
import io


def test_upload_novel_success(client: TestClient, auth_headers):
    """测试上传小说成功"""
    # 创建测试文件
    file_content = b"This is a test novel content."
    file = ("test.txt", file_content, "text/plain")

    response = client.post(
        "/api/upload/novel",
        headers=auth_headers,
        files={"file": file},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "上传成功"
    assert data["data"]["title"] == "test"
    assert data["data"]["file_size"] == len(file_content)


def test_upload_novel_unauthorized(client: TestClient):
    """测试未认证上传小说失败"""
    file = ("test.txt", b"content", "text/plain")
    response = client.post(
        "/api/upload/novel",
        files={"file": file},
    )
    assert response.status_code == 401


def test_upload_novel_invalid_format(client: TestClient, auth_headers):
    """测试上传非 TXT 格式失败"""
    file = ("test.pdf", b"content", "application/pdf")
    response = client.post(
        "/api/upload/novel",
        headers=auth_headers,
        files={"file": file},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 400
    assert "仅支持 TXT 格式" in data["message"]


def test_list_novels_success(client: TestClient, auth_headers):
    """测试获取小说列表成功"""
    # 先上传一个小说
    file = ("test.txt", b"content", "text/plain")
    client.post(
        "/api/upload/novel",
        headers=auth_headers,
        files={"file": file},
    )

    # 获取列表
    response = client.get("/api/novels", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]["items"]) > 0


def test_list_novels_unauthorized(client: TestClient):
    """测试未认证获取小说列表失败"""
    response = client.get("/api/novels")
    assert response.status_code == 401


def test_delete_novel_success(client: TestClient, auth_headers):
    """测试删除小说成功"""
    # 先上传一个小说
    file = ("test.txt", b"content", "text/plain")
    upload_response = client.post(
        "/api/upload/novel",
        headers=auth_headers,
        files={"file": file},
    )
    novel_id = upload_response.json()["data"]["id"]

    # 删除小说
    response = client.delete(f"/api/novels/{novel_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "删除成功"


def test_delete_novel_not_found(client: TestClient, auth_headers):
    """测试删除不存在的小说"""
    response = client.delete("/api/novels/999", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 404
    assert "小说不存在" in data["message"]


def test_delete_novel_unauthorized(client: TestClient):
    """测试未认证删除小说失败"""
    response = client.delete("/api/novels/1")
    assert response.status_code == 401

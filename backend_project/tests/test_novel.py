"""
小说 API 测试（适配权限系统 REQ-P3-004）

上传需要 seed_member 最低角色，列表需要登录，删除需所有者或管理员。
"""
import pytest
from fastapi.testclient import TestClient


class TestUploadNovel:
    """POST /api/upload/novel — 上传小说（需 seed_member）"""

    def test_upload_success(self, client: TestClient, seed_headers):
        """种子成员上传小说成功"""
        file_content = b"This is a test novel content."
        file = ("test.txt", file_content, "text/plain")

        response = client.post(
            "/api/upload/novel",
            headers=seed_headers,
            files={"file": file},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "上传成功"
        assert data["data"]["title"] == "test"
        assert data["data"]["file_size"] == len(file_content)

    def test_upload_member_rejected(self, client: TestClient, auth_headers):
        """普通成员上传被拒"""
        file = ("test.txt", b"content", "text/plain")
        response = client.post(
            "/api/upload/novel",
            headers=auth_headers,
            files={"file": file},
        )
        assert response.status_code == 403

    def test_upload_unauthorized(self, client: TestClient):
        """未认证上传失败"""
        file = ("test.txt", b"content", "text/plain")
        response = client.post(
            "/api/upload/novel",
            files={"file": file},
        )
        assert response.status_code in (401, 403)

    def test_upload_invalid_format(self, client: TestClient, seed_headers):
        """非 TXT 格式文件上传失败"""
        file = ("test.pdf", b"content", "application/pdf")
        response = client.post(
            "/api/upload/novel",
            headers=seed_headers,
            files={"file": file},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 400
        assert "仅支持 TXT 格式" in data["message"]


class TestListNovels:
    """GET /api/novels — 获取小说列表（需登录）"""

    def test_list_with_novel(self, client: TestClient, seed_headers):
        """上传小说后列表应有数据"""
        # 先上传
        client.post(
            "/api/upload/novel",
            headers=seed_headers,
            files={"file": ("test.txt", b"content", "text/plain")},
        )

        response = client.get("/api/novels", headers=seed_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) > 0

    def test_list_unauthorized(self, client: TestClient):
        """未认证获取小说列表"""
        response = client.get("/api/novels")
        assert response.status_code in (401, 403)


class TestDeleteNovel:
    """DELETE /api/novels/{id} — 删除小说"""

    def test_delete_success(self, client: TestClient, seed_headers):
        """所有者可删除自己的小说"""
        # 上传
        upload_resp = client.post(
            "/api/upload/novel",
            headers=seed_headers,
            files={"file": ("test.txt", b"content", "text/plain")},
        )
        novel_id = upload_resp.json()["data"]["id"]

        response = client.delete(f"/api/novels/{novel_id}", headers=seed_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "删除成功"

    def test_delete_not_found(self, client: TestClient, seed_headers):
        """删除不存在的小说"""
        response = client.delete("/api/novels/999", headers=seed_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 404
        assert "小说不存在" in data["message"]

    def test_delete_unauthorized(self, client: TestClient):
        """未认证删除失败"""
        response = client.delete("/api/novels/1")
        assert response.status_code in (401, 403)

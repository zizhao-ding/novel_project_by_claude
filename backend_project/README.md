# 后端项目 (Backend Project)

小说阅读平台的后端服务，基于 Python + FastAPI + SQLite 构建。

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| Web 框架 | FastAPI | 高性能异步 Web 框架 |
| 数据库 | SQLite | 轻量级嵌入式数据库 |
| ORM | SQLModel | SQLAlchemy + Pydantic 结合 |
| 密码加密 | bcrypt | 密码哈希存储 |
| ASGI 服务器 | Uvicorn | 高性能异步服务器 |

## 项目结构

```
backend_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── database.py          # 数据库连接配置
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py          # 认证相关接口
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # 用户数据模型
│   └── schemas/
│       ├── __init__.py
│       └── user.py          # 请求/响应模型
├── .env.example             # 环境变量示例
├── requirements.txt         # Python 依赖
└── README.md                # 本文档
```

## 环境要求

- Python 3.9+
- pip

## 快速开始

### 1. 安装依赖

```bash
cd backend_project
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

```bash
cp .env.example .env
```

默认使用 SQLite 数据库文件 `app.db`，无需额外配置即可运行。

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

启动成功后访问：
- 服务地址：http://localhost:8000
- API 文档（Swagger）：http://localhost:8000/docs
- API 文档（ReDoc）：http://localhost:8000/redoc

## API 接口

### 健康检查

```
GET /
```

响应示例：
```json
{
  "status": "ok",
  "message": "后端服务运行中"
}
```

### 用户注册

```
POST /api/auth/register
Content-Type: application/json
```

请求体：
```json
{
  "username": "testuser",
  "password": "123456"
}
```

参数说明：

| 字段 | 类型 | 必填 | 限制 | 说明 |
|------|------|------|------|------|
| username | string | 是 | 3-100 字符 | 账号 |
| password | string | 是 | 6-128 字符 | 密码 |

成功响应：
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "created_at": "2026-06-20T10:30:00"
  }
}
```

失败响应（账号已存在）：
```json
{
  "code": 400,
  "message": "该账号已被注册",
  "data": null
}
```

### 测试接口

使用 curl 测试注册接口：

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "123456"}'
```

也可以直接访问 http://localhost:8000/docs 在 Swagger UI 中测试。

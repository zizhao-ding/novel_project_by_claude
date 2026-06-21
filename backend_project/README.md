# 后端项目 (Backend Project)

小说阅读平台的后端服务，基于 Python + FastAPI + SQLite 构建。

---

## VS Code 查看 SQLite 数据库

推荐安装 **SQLite Viewer** 插件，在 VS Code 中直接查看和编辑数据库：

1. 打开 VS Code 扩展商店（`Cmd+Shift+X` / `Ctrl+Shift+X`）
2. 搜索 **SQLite Viewer**（作者：qwtel）
3. 点击安装
4. 安装后在左侧文件列表中找到 `app.db`，右键 → **Open with SQLite Viewer**
5. 即可浏览表结构、查询数据、编辑记录

> 其他可选插件：**SQLite**（作者：alexcvzz）也支持直接打开 `.db` 文件。

---

## 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| Web 框架 | FastAPI | 高性能异步 Web 框架 |
| 数据库 | SQLite | 轻量级嵌入式数据库 |
| ORM | SQLModel | SQLAlchemy + Pydantic 结合 |
| 密码加密 | bcrypt | 密码哈希存储 |
| JWT | python-jose | Token 签发与验证 |
| ASGI 服务器 | Uvicorn | 高性能异步服务器 |

## 项目结构

```
backend_project/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口 + CORS
│   ├── database.py          # 数据库连接配置
│   ├── config.py            # JWT 密钥/算法/过期时间配置
│   ├── api/
│   │   ├── __init__.py
│   │   └── auth.py          # 认证接口（注册/登录/资料）
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # 用户数据模型
│   └── schemas/
│       ├── __init__.py
│       └── user.py          # 请求/响应 Pydantic 模型
├── .env                     # 环境变量（JWT 密钥等）
├── .env.example             # 环境变量模板
├── requirements.txt         # Python 依赖
└── README.md                # 本文档
```

## 环境要求

- Python 3.9+

---

## 快速开始

### macOS

```bash
# 1. 进入后端目录
cd backend_project

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip3 install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env

# 5. 启动服务
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Windows

```cmd
:: 1. 进入后端目录
cd backend_project

:: 2. 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

:: 3. 安装依赖
pip install -r requirements.txt

:: 4. 配置环境变量
copy .env.example .env

:: 5. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 验证启动

```bash
curl http://localhost:8000/
# 返回 {"status":"ok","message":"后端服务运行中"}
```

### 停止服务

按 `Ctrl + C`。

---

## API 文档

启动后访问：http://localhost:8000/docs （Swagger UI，可直接在网页中测试所有接口）

---

## API 接口

### 健康检查

```
GET /
```

响应：
```json
{ "status": "ok", "message": "后端服务运行中" }
```

---

### 用户注册

```
POST /api/auth/register
```

| 字段 | 类型 | 必填 | 限制 | 说明 |
|------|------|------|------|------|
| username | string | 是 | 3-100 字符 | 账号 |
| password | string | 是 | 6-128 字符 | 密码 |

成功响应 `code=0`：
```json
{
  "code": 0,
  "message": "注册成功",
  "data": { "id": 1, "username": "testuser", "created_at": "2026-06-21T10:30:00" }
}
```

失败响应 `code=400`（账号已存在）：
```json
{ "code": 400, "message": "该账号已被注册", "data": null }
```

---

### 用户登录

```
POST /api/auth/login
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 账号 |
| password | string | 是 | 密码 |

成功响应 `code=0`：
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGci...",
    "user": { "id": 1, "username": "testuser", "created_at": "2026-06-21T10:30:00" }
  }
}
```

失败响应 `code=400`（用户名或密码错误）：
```json
{ "code": 400, "message": "用户名或密码错误", "data": null }
```

> 登录成功后将 `token` 存储在客户端，后续请求在 `Authorization: Bearer <token>` 头中携带。

---

### 获取用户资料

```
GET /api/auth/profile
Authorization: Bearer <token>
```

成功响应：
```json
{
  "code": 0,
  "message": "获取成功",
  "data": { "id": 1, "username": "testuser", "created_at": "2026-06-21T10:30:00" }
}
```

---

## curl 测试命令

```bash
# 注册
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 登录
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 获取资料（替换 TOKEN 为登录返回的 token）
curl http://localhost:8000/api/auth/profile \
  -H "Authorization: Bearer TOKEN"
```

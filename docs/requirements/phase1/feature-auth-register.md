# REQ-P1-001: 用户注册与登录

> **状态**: ✅ 已完成
> **优先级**: P0 核心
> **创建日期**: 2026-06-25
> **最后更新**: 2026-06-25

## 1. 概述

实现用户注册、登录、登出及登录状态持久化功能。这是整个应用的基础模块，所有需要用户身份的功能（上传、书签等）都依赖此模块。

## 2. 用户故事

- 作为 **新用户**，我想要 **注册账号**，以便 **使用平台的全部功能**
- 作为 **已有账号用户**，我想要 **登录**，以便 **访问我的个人数据和藏书**
- 作为 **登录用户**，我想要 **退出登录**，以便 **保护我的账号安全**
- 作为 **用户**，我想要 **记住登录状态**，以便 **刷新页面后不需要重新登录**

## 3. UI 布局

### 登录页
```
┌──────────────────────────────────────────┐
│                                          │
│         🎨 小说阅读平台 (Logo)            │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  登录                              │  │
│  │                                    │  │
│  │  用户名: [________________]        │  │
│  │  密码:   [________________]        │  │
│  │                                    │  │
│  │  [x] 记住我                        │  │
│  │                                    │  │
│  │  [      登  录      ]              │  │
│  │                                    │  │
│  │  没有账号？[立即注册]               │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

### 注册页
```
┌──────────────────────────────────────────┐
│  ┌────────────────────────────────────┐  │
│  │  注册                              │  │
│  │                                    │  │
│  │  用户名: [________________]        │  │
│  │  邮箱:   [________________]        │  │
│  │  密码:   [________________]        │  │
│  │  确认密码: [______________]        │  │
│  │                                    │  │
│  │  [      注  册      ]              │  │
│  │                                    │  │
│  │  已有账号？[立即登录]               │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## 4. 路由 & 页面

| 路由路径 | 页面名称 | 视图文件 | 认证要求 |
|----------|----------|----------|----------|
| `/login` | `Login` | `LoginView.vue` | 否 |
| `/register` | `Register` | `RegisterView.vue` | 否 |

## 5. 组件树

```
LoginView.vue
├── ElCard                         # 登录卡片容器
│   ├── ElForm                     # 登录表单
│   │   ├── ElFormItem (用户名)
│   │   │   └── ElInput (v-model, 校验: 必填)
│   │   ├── ElFormItem (密码)
│   │   │   └── ElInput (type="password", 校验: 必填, 长度≥6)
│   │   ├── ElCheckbox (记住我)
│   │   └── ElButton (type="primary", :loading, @click=handleLogin)
│   └── 跳转链接 → /register

RegisterView.vue
├── ElCard                         # 注册卡片容器
│   ├── ElForm                     # 注册表单
│   │   ├── ElFormItem (用户名)
│   │   ├── ElFormItem (邮箱)
│   │   ├── ElFormItem (密码)
│   │   ├── ElFormItem (确认密码)
│   │   └── ElButton (type="primary", @click=handleRegister)
│   └── 跳转链接 → /login
```

## 6. 数据流 & Store 设计

### Store: `useUserStore`

```
State:
  user: User | null           # 当前用户信息
  token: string | null        # JWT Token（持久化到 localStorage）
  isAuthenticated: boolean    # computed: !!token

Actions:
  login(username, password)   # 登录 → 存储 token → 获取用户信息
  register(data)              # 注册 → 自动登录
  logout()                    # 清除 token → 清除用户信息 → 跳转登录页
  fetchProfile()              # 获取当前用户信息
```

### Token 持久化

```typescript
// token 存储在 localStorage，store 初始化时读取
const token = ref(localStorage.getItem('token'));

// 登录成功后写入
localStorage.setItem('token', newToken);

// 登出时清除
localStorage.removeItem('token');
```

## 7. API 契约

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/auth/register` | 注册 | `{ username, email, password }` | `{ user: User, token: string }` |
| POST | `/api/auth/login` | 登录 | `{ username, password }` | `{ user: User, token: string }` |
| GET | `/api/auth/profile` | 获取用户信息 | Header: `Authorization: Bearer <token>` | `User` |

> 后端已实现全部认证接口：`POST /api/auth/register`、`POST /api/auth/login`、`GET /api/auth/profile`。

## 8. 验收标准

### 场景 1: 用户注册成功

- [x] 用户在注册页填写合法用户名、邮箱、密码并提交
- [x] 系统调用注册 API
- [x] 注册成功后自动跳转到首页
- [x] 显示"注册成功"提示
- [x] 导航栏显示用户名（已登录状态）

### 场景 2: 注册表单校验

- [x] 用户提交空表单时显示校验错误
- [x] 两次密码不一致时显示校验错误
- [x] 密码少于6位时显示校验错误
- [x] 校验失败时不发起 API 请求

### 场景 3: 用户登录成功

- [x] 用户在登录页输入正确的用户名和密码并提交
- [x] 系统调用登录 API
- [x] 登录成功后跳转到首页（或 redirect 目标页）
- [x] 显示"登录成功"提示
- [x] token 写入 localStorage

### 场景 4: 登录失败

- [x] 用户输入错误的密码
- [x] 显示"用户名或密码错误"提示
- [x] 不跳转页面

### 场景 5: 登录状态持久化

- [x] 用户已登录（localStorage 中有有效 token）
- [x] 刷新页面后自动读取 token 并获取用户信息
- [x] 保持登录状态

### 场景 6: 未登录访问受限页面

- [x] 用户未登录时尝试访问 /library
- [x] 自动跳转到 /login?redirect=/library
- [x] 登录后自动跳转回 /library

## 9. 技术实现要点

- [x] 表单校验使用 Element Plus Form 的 rules 属性
- [x] 登录/注册按钮需 loading 状态防止重复提交
- [x] Token 通过 Axios 请求拦截器自动附加
- [x] 401 响应通过 Axios 响应拦截器统一处理（清除 token + 跳转登录）
- [x] 密码在前端做一次 SHA256 哈希后再发送（使用 crypto-js）
- [x] 路由守卫在 `router/guards.ts` 中实现
- [x] 首页（HomeView）含登录/登出状态展示
- [x] 后端登录 API（`POST /api/auth/login`）已实现
- [x] 后端 profile API（`GET /api/auth/profile`）已实现
- [x] 后端 JWT Token 签发和验证
- [x] 后端密码 bcrypt 哈希存储

## 10. 后端实现

### 数据模型

```python
# backend_project/app/models/user.py
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str  # 明文密码（仅用于传输）
    password_hash: str  # bcrypt 哈希后的密码
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### API 实现

| 端点 | 文件 | 说明 | 状态 |
|------|------|------|------|
| `POST /api/auth/register` | `backend_project/app/api/auth.py` | 用户注册 | ✅ 已实现 |
| `POST /api/auth/login` | `backend_project/app/api/auth.py` | 用户登录（JWT） | ✅ 已实现 |
| `GET /api/auth/profile` | `backend_project/app/api/auth.py` | 获取用户信息 | ✅ 已实现 |

### 数据库设计

| 表名 | 字段 | 索引 |
|------|------|------|
| `users` | id, username, password, password_hash, created_at, updated_at | username (unique) |

### 依赖

- `bcrypt`: 密码哈希（`pip install bcrypt`）
- `python-jose`: JWT Token 签发和验证（`pip install python-jose`）
- `sqlmodel`: ORM（`pip install sqlmodel`）

### 配置

```python
# backend_project/app/config.py
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 11. 参考 & 备注

- **核心规范**: `docs/specs/core/coding-standards.md`
- **架构规范**: `docs/specs/core/architecture.md`
- **Hook 规则**: `docs/specs/core/hook-rules.md`
- **后端实现**: `backend_project/app/api/auth.py`（注册、登录、profile 全部实现）
- **前端实现**: `front_project/src/views/LoginView.vue`、`RegisterView.vue`、`HomeView.vue`
- **Store 实现**: `front_project/src/stores/user.ts`
- **密码哈希**: 后端使用 bcrypt，前端使用 crypto-js SHA256
- **JWT 配置**: `backend_project/app/config.py`

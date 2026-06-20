# 用户注册与登录

> **状态**: 🚧 开发中
> **优先级**: P0 核心
> **关联 Spec**: 无

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

> 后端已实现 `POST /api/auth/register` 端点，登录和 profile 端点待实现。

## 8. 验收标准

### 场景 1: 用户注册成功

```
Given 用户在注册页
When  用户填写合法用户名、邮箱、密码并提交
Then  系统调用注册 API
      注册成功后自动跳转到首页
      显示"注册成功"提示
      导航栏显示用户名（已登录状态）
```

### 场景 2: 注册表单校验

```
Given 用户在注册页
When  用户提交空表单 / 两次密码不一致 / 密码少于6位
Then  表单显示对应的校验错误提示
      不会发起 API 请求
```

### 场景 3: 用户登录成功

```
Given 用户在登录页
When  用户输入正确的用户名和密码并提交
Then  系统调用登录 API
      登录成功后跳转到首页（或 redirect 目标页）
      显示"登录成功"提示
      token 写入 localStorage
```

### 场景 4: 登录失败

```
Given 用户在登录页
When  用户输入错误的密码
Then  显示"用户名或密码错误"提示
      不跳转页面
```

### 场景 5: 登录状态持久化

```
Given 用户已登录（localStorage 中有有效 token）
When  用户刷新页面
Then  自动读取 token 并获取用户信息
      保持登录状态
```

### 场景 6: 未登录访问受限页面

```
Given 用户未登录
When  用户尝试访问 /library（需要登录的页面）
Then  自动跳转到 /login?redirect=/library
      登录后自动跳转回 /library
```

## 9. 技术实现要点

- [x] 表单校验使用 Element Plus Form 的 rules 属性
- [x] 登录/注册按钮需 loading 状态防止重复提交
- [x] Token 通过 Axios 请求拦截器自动附加
- [x] 401 响应通过 Axios 响应拦截器统一处理（清除 token + 跳转登录）
- [x] 密码在前端做一次 SHA256 哈希后再发送（使用 crypto-js）
- [x] 路由守卫在 `router/guards.ts` 中实现
- [x] 首页（HomeView）含登录/登出状态展示
- [ ] 后端登录 API（`POST /api/auth/login`）待实现
- [ ] 后端 profile API（`GET /api/auth/profile`）待实现

## 10. 参考 & 备注

- 相关 Rules: `02_vue3_components.md`, `04_state_management.md`, `05_api_services.md`, `07_routing.md`
- 后端已实现: `POST /api/auth/register`（`backend_project/app/api/auth.py`）
- 密码哈希: 后端使用 bcrypt，前端使用 crypto-js SHA256

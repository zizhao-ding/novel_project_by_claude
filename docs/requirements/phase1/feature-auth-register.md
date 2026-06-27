# REQ-P1-001: 用户注册与登录

> **状态**: ✅ done
> **优先级**: P0
> **创建日期**: 2026-06-25
> **最后更新**: 2026-06-27

## 1. 概述

实现用户注册与登录功能，包括两栏清新风格页面、表单校验、JWT 认证、注册时头像选择等。采用前后端分离架构，前端使用 Vue 3 + Element Plus，后端使用 FastAPI + SQLModel + SQLite。

## 2. 用户故事

- 作为 **新用户**，我想要 **注册账号并选择头像**，以便 **个性化我的身份**
- 作为 **已注册用户**，我想要 **登录系统**，以便 **访问需要认证的功能**
- 作为 **已登录用户**，我想要 **保持登录状态**，以便 **避免重复登录**
- 作为 **已登录用户**，我想要 **退出登录**，以便 **保护账号安全**

## 3. UI 布局

### 登录页 / 注册页（两栏布局）

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │   📖 Logo    │    │   欢迎回来 👋 / 创建账号✨ │   │
│  │  小说阅读平台 │    │                          │   │
│  │              │    │   用户名                  │   │
│  │  发现好书，   │    │   密码                    │   │  ← 右侧表单
│  │  沉浸阅读    │    │   [登录/注册]             │   │
│  │              │    │   没有账号？立即注册       │   │
│  │  📕📗📘📙   │    │                          │   │
│  │  (漂浮动画)  │    │                          │   │
│  └──────────────┘    └──────────────────────────┘   │
│   ← 左侧品牌区（绿色渐变）→                           │
└─────────────────────────────────────────────────────┘
```

### 注册页头像选择

```
选择头像:
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│ 🟡 │ │ 💗 │ │ 💙 │ │ 🟢 │ │ 🔴 │ │ 💜 │ │ 🟡 │ │ 🟢 │
│ A  │ │ A  │ │ A  │ │ A  │ │ A  │ │ A  │ │ A  │ │ A  │
└────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
  ✓ — 实时预览用户名首字母
```

## 4. 路由 & 页面

| 路由路径 | 页面名称 | 视图文件 | 认证要求 |
|----------|----------|----------|----------|
| `/login` | `Login` | `LoginView.vue` | 否 |
| `/register` | `Register` | `RegisterView.vue` | 否 |

## 5. 组件树

```
LoginView.vue / RegisterView.vue
├── brand-panel              # 左侧品牌区（绿色渐变 + Logo + 漂浮书本）
│   ├── logo                 # 📖 + 小说阅读平台
│   ├── slogan               # "发现好书，沉浸阅读"
│   └── illustration         # 📕📗📘📙 漂浮动画
└── form-panel               # 右侧表单区
    ├── title                # "欢迎回来 👋" / "创建账号 ✨"
    ├── el-form              # 表单
    │   ├── avatar-picker    # 头像选择器（仅注册页）
    │   ├── el-input 用户名
    │   ├── el-input 密码
    │   ├── el-input 确认密码（仅注册页）
    │   └── el-button 提交
    └── switch-link          # 切换登录/注册链接
```

## 6. 数据流 & Store 设计

### Store: `useUserStore`

```typescript
State:
  user: User | null           # 当前用户信息
  token: string | null        # JWT Token（持久化到 localStorage）
  loading: boolean            # 请求加载状态
  error: string | null        # 错误信息

Getters:
  isAuthenticated: boolean    # 是否已登录

Actions:
  register(username, password, avatar)  # 注册
  login(username, password)             # 登录
  logout()                              # 退出登录（含确认弹窗）
  fetchProfile()                        # 获取用户信息
```

### 数据结构

```typescript
type UserRole = 'admin' | 'seed_member' | 'member';

interface User {
  id: number;
  username: string;
  role: UserRole;
  avatar: string;       // 颜色值，如 "#F5A623"
  created_at: string;
}

const AVATAR_PRESETS = [
  '#F5A623', '#F78DA7', '#8BD3DD', '#A8D8B9',
  '#FF6B6B', '#C9B1FF', '#FFD93D', '#6BCB77',
];
```

## 7. API 契约

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/auth/register` | 用户注册 | `{ username, password, avatar }` | `{ code, message, data: User }` |
| POST | `/api/auth/login` | 用户登录 | `{ username, password }` | `{ code, message, data: { token, User } }` |
| GET | `/api/auth/profile` | 获取当前用户 | - | `{ code, message, data: User }` |
| GET | `/api/auth/user/stats` | 用户统计 | - | `{ code, message, data: UserStats }` |

## 8. 验收标准

### 注册

- [x] 两栏布局：左侧品牌区（绿色渐变 + Logo + 漂浮书本），右侧表单区
- [x] 注册页显示头像选择器（8 种预设颜色）
- [x] 头像选择器实时预览用户名首字母
- [x] 选中头像有绿色外框 + 勾选图标
- [x] 用户名：3-100 个字符，必填
- [x] 密码：至少 6 位，必填
- [x] 确认密码：必须与密码一致
- [x] 注册成功后跳转登录页
- [x] 用户名已存在时返回错误提示
- [x] 头像颜色保存到后端 User 模型

### 登录

- [x] 两栏布局，风格与注册页一致
- [x] 登录表单：用户名 + 密码
- [x] 登录成功后存储 JWT Token 到 localStorage
- [x] 登录成功后跳转到 redirect 目标页或首页
- [x] 用户名或密码错误时返回错误提示
- [x] 支持 Enter 键提交

### 全局

- [x] 路由守卫：未登录访问需认证页面时跳转登录页
- [x] 退出登录二次确认
- [x] Token 过期时自动清除登录状态
- [x] 全局头像使用用户选择的颜色

## 9. 技术实现要点

### 前端
- [x] 两栏布局（品牌区 + 表单区）
- [x] 绿色系清新风格（#e8f5e9 → #81c784 渐变）
- [x] 漂浮书本 CSS 动画（@keyframes float）
- [x] Element Plus el-form 表单校验
- [x] el-input 圆角样式覆盖（:deep）
- [x] 头像选择器（AVATAR_PRESETS 颜色数组）
- [x] JWT Token 持久化（localStorage）
- [x] 路由守卫（router/guards.ts）
- [x] Pinia Setup Store 模式

### 后端
- [x] User 模型（含 role、avatar 字段）
- [x] bcrypt 密码哈希
- [x] JWT Token 生成与验证（python-jose）
- [x] CORS 中间件
- [x] 统一响应格式 `{ code, message, data }`

## 10. 参考 & 备注

- **前端实现**: `frontend_project/src/views/LoginView.vue`, `RegisterView.vue`
- **Store 实现**: `frontend_project/src/stores/user.ts`
- **API 实现**: `frontend_project/src/services/auth.ts`
- **后端实现**: `backend_project/app/api/auth.py`
- **数据模型**: `backend_project/app/models/user.py`
- **Schema**: `backend_project/app/schemas/user.py`
- **路由守卫**: `frontend_project/src/router/guards.ts`

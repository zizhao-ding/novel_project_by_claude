# 认证模块规范

> **优先级**: P0 - 必须遵守
> **最后更新**: 2026-06-28
> **覆盖范围**: 前端 + 后端认证全链路

## 1. 模块架构

```
┌─────────────── 前端 ───────────────────────────────────────────┐
│  LoginView / RegisterView                                      │
│      ↓                                                         │
│  stores/user.ts  (token localStorage 持久化)                     │
│      ↓                                                         │
│  services/auth.ts  (register / login / profile / stats / chpwd) │
│      ↓                                                         │
│  services/api.ts  (请求拦截器自动附加 Bearer token)              │
│      ↓                                                         │
│  router/guards.ts  (requiresAuth → 重定向 /login)               │
└────────────────────────────────────────────────────────────────┘
                          │ HTTP
                          ▼
┌─────────────── 后端 ───────────────────────────────────────────┐
│  POST /api/auth/register    注册                                │
│  POST /api/auth/login       登录 → 返回 JWT                     │
│  GET  /api/auth/profile     当前用户信息                         │
│  GET  /api/auth/user/stats  用户统计                             │
│  POST /api/auth/change-password  修改密码                       │
│                                                                │
│  JWT 签发: create_access_token(user_id)                        │
│  JWT 验证: decode_access_token(token)                          │
│  密码: bcrypt.hashpw / bcrypt.checkpw                          │
│  权限: get_current_user → require_role / require_min_role       │
└────────────────────────────────────────────────────────────────┘
```

## 2. 用户模型

### 数据库 (SQLModel)

```python
# app/models/user.py
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    username: str = Field(unique=True, index=True, max_length=100)
    password_hash: str = Field(max_length=255)
    role: str = Field(default="member")      # admin / seed_member / member
    avatar: Optional[str] = Field(default=None)  # 颜色 hex 值
    created_at: datetime
    updated_at: datetime
```

### 前端类型

```typescript
// types/user.ts
type UserRole = 'admin' | 'seed_member' | 'member';

interface User {
  id: number;
  username: string;
  role: UserRole;
  avatar: string | null;
  created_at: string;
}
```

## 3. JWT 认证流程

```
注册: username + password → bcrypt hash → 存入 DB → 返回 User
登录: username + password → bcrypt verify → JWT(exp=24h) → 返回 token + user
请求: Authorization: Bearer <token> → decode → get_current_user → 注入路由
过期: 前端拦截器 401 → clearToken → 重定向 /login
```

### JWT 配置

```python
# app/config.py
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 小时
```

## 4. 前端 Token 管理

```typescript
// stores/user.ts
// 初始化时从 localStorage 恢复
const token = ref<string | null>(localStorage.getItem('token'));

// 登录成功时持久化
function setToken(newToken: string) {
  token.value = newToken;
  localStorage.setItem('token', newToken);
}

// 退出时清除
function logout() {
  token.value = null;
  user.value = null;
  localStorage.removeItem('token');
}
```

```typescript
// services/api.ts 请求拦截器
this.instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## 5. 路由守卫

```typescript
// router/guards.ts
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  // 1. 需要登录但未登录 → 重定向登录页
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } });
  }

  // 2. 已登录但访问登录/注册 → 重定向首页
  if (userStore.isAuthenticated && ['Login', 'Register'].includes(to.name as string)) {
    return next({ name: 'Home' });
  }

  // 3. 角色检查
  if (to.meta.requiredRole) {
    const roleLevel = { member: 0, seed_member: 1, admin: 2 };
    if (roleLevel[userStore.user!.role] < roleLevel[to.meta.requiredRole]) {
      return next({ name: 'Home' });
    }
  }

  next();
});
```

## 6. 密码安全

| 环节 | 方法 |
|------|------|
| 注册存储 | `bcrypt.hashpw(password.encode(), bcrypt.gensalt())` |
| 登录验证 | `bcrypt.checkpw(password.encode(), user.password_hash.encode())` |
| 传输 | HTTP（开发阶段），生产需 HTTPS |
| 修改密码 | 需验证旧密码正确 + 新密码 != 旧密码 |

## 7. 头像系统

- 注册时从 8 色预设中选择（`AVATAR_PRESETS`）
- 存储为颜色 hex 值（如 `#409eff`）
- 前端显示为首字母占位 + 背景色
- 与 AppHeader / UserView / 悬浮卡片联动

## 8. 验收清单

- [ ] 注册：用户名唯一，密码 6-20 位，头像 8 色可选
- [ ] 登录：JWT 签发，token 持久化，刷新不丢失
- [ ] 路由守卫：未登录拦截 + 登录后重定向回原页面
- [ ] 401 处理：token 过期自动清除并跳转登录
- [ ] 修改密码：旧密码正确才能更新
- [ ] 角色：admin / seed_member / member 三级

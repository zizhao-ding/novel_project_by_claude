# REQ-P3-004: 权限系统 — 角色分级 + 小说可见性 + 角色管理

> **状态**: 📝 pending
> **优先级**: P0（基础设施，所有功能依赖）
> **创建日期**: 2026-06-28
> **最后更新**: 2026-06-28

## 1. 概述

建立三级角色权限体系，控制用户对小说内容的访问范围。同时为小说增加可见性标签，实现差异化内容分发。新增管理员专属的用户角色管理页面。

**设计原则**：简单实用，不过度设计。三级角色足够覆盖当前需求。

## 2. 角色定义

| 角色 | 标识 | 获取方式 | 定位 |
|------|------|----------|------|
| 管理员 | `admin` | 数据库手动设置 | 超级管理员，管理用户角色和全站内容 |
| 种子成员 | `seed_member` | 管理员提升 | 受信任的贡献者，可上传/下载，可看种子内容 |
| 普通成员 | `member` | 注册默认角色 | 普通读者，书架内阅读，只看公开内容 |

> 现有注册接口已默认 `member`，无需改动。admin 通过种子数据脚本设置。

## 3. 权限矩阵

| 能力 | 未登录 | 普通成员 | 种子成员 | 管理员 |
|------|:---:|:---:|:---:|:---:|
| 浏览首页/热门/搜索 | ✅ | ✅ | ✅ | ✅ |
| 查看公开小说详情 | ✅ | ✅ | ✅ | ✅ |
| 阅读小说 | ❌ | ⚠️ 仅书架内 | ✅ 全部 | ✅ 全部 |
| 下载 TXT 原文件 | ❌ | ❌ | ✅ | ✅ |
| 上传小说 | ❌ | ❌ | ✅ | ✅ |
| 管理个人书架 | ❌ | ✅ | ✅ | ✅ |
| 管理个人分类 | ❌ | ✅ | ✅ | ✅ |
| 删除自己的小说 | ❌ | ❌ | ✅ | ✅ |
| 查看种子内容 | ❌ | ❌ | ✅ | ✅ |
| 查看管理内容 | ❌ | ❌ | ❌ | ✅ |
| 删除任何小说 | ❌ | ❌ | ❌ | ✅ |
| 管理用户角色 | ❌ | ❌ | ❌ | ✅ |

## 4. 小说可见性标签

### 4.1 概念

每本小说新增 `visibility` 字段，控制哪些角色可以看到和阅读该小说。

| 等级 | 值 | 含义 | 谁能看 |
|------|------|------|--------|
| 公开 | `public` | 所有人可见（默认） | 所有人 |
| 种子 | `seed` | 种子用户可见 | 种子成员 + 管理员 |
| 管理 | `admin` | 仅管理员可见 | 仅管理员 |

### 4.2 作用范围

小说可见性影响以下场景：
- 首页热门推荐 / 最新上传 → 只展示当前用户可见的小说
- 搜索结果 → 只返回当前用户可见的小说
- 书房列表 → 只显示当前用户可见的小说
- 阅读器 → 无权访问的小说返回 403

### 4.3 设置方式

- 上传时默认 `public`
- 管理员上传时可选择 `seed` 或 `admin`
- 管理员可在管理后台修改已有小说的可见性

## 5. 用户角色管理页

### 5.1 UI 布局

```
┌──────────────────────────────────────────────────────┐
│ ← 返回    👥 用户管理                                 │  ← 顶栏（AppHeader）
├──────────────────────────────────────────────────────┤
│                                                      │
│  搜索: [___________]  🔍                             │
│                                                      │
│  ┌──────────────────────────────────────────────────┐│
│  │ ID │ 用户名    │ 角色      │ 注册时间     │ 操作 ││
│  ├──────────────────────────────────────────────────┤│
│  │ 1  │ test      │ [管理员 ▼] │ 2026-06-25  │ 保存 ││  ← 角色下拉框
│  │ 2  │ alice     │ [种子成员▼]│ 2026-06-26  │ 保存 ││
│  │ 3  │ bob       │ [普通成员▼]│ 2026-06-27  │ 保存 ││
│  │ 4  │ charlie   │ [普通成员▼]│ 2026-06-28  │ 保存 ││
│  └──────────────────────────────────────────────────┘│
│                                                      │
│  共 4 个用户                          ← 1/1 页 →     │
└──────────────────────────────────────────────────────┘
```

### 5.2 交互说明

| 操作 | 说明 |
|------|------|
| 搜索 | 按用户名模糊搜索 |
| 角色下拉 | 选择后点"保存"生效，调用后端接口修改 |
| 权限控制 | 仅管理员可访问此页面 |
| 自我保护 | 管理员不能降级自己（防止锁死） |

## 6. 路由 & 页面

| 路由 | 页面 | 权限 | 说明 |
|------|------|------|------|
| `/admin/users` | `AdminUsersView.vue`（新增） | 仅 admin | 用户角色管理 |
| `/reader/:id` | `ReaderView.vue` | 需登录 | 增加可见性检查 |
| `/library` | `LibraryView.vue` | 需登录 | 增加可见性过滤 |
| `/upload` | `UploadView.vue` | 需登录 | 上传入口（仅 seed+ 有权限） |

> `/search`、`/` 等公开页面也需按角色过滤返回内容。

## 7. 后端实现

### 7.1 数据库变更

#### Novel 模型新增字段
```python
# models/novel.py
visibility: str = Field(default="public", max_length=20,
    description="可见性: public / seed / admin")
```

#### 无需新增表
- 角色信息已存在 User 模型的 `role` 字段
- 无需权限中间表，直接判断角色即可

### 7.2 新增权限依赖函数

```python
# app/api/auth.py 新增

def require_role(*allowed_roles: str):
    """依赖工厂：仅允许指定角色访问"""
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user
    return checker

def require_min_role(min_role: str):
    """依赖工厂：角色等级不低于指定级别"""
    ROLE_LEVEL = {"member": 0, "seed_member": 1, "admin": 2}
    def checker(current_user: User = Depends(get_current_user)):
        if ROLE_LEVEL.get(current_user.role, 0) < ROLE_LEVEL.get(min_role, 0):
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user
    return checker

def get_visible_novels_query(user: User, session: Session):
    """根据用户角色返回可见的小说查询"""
    query = select(Novel)
    if user.role == "admin":
        return query  # 管理员看全部
    elif user.role == "seed_member":
        return query.where(Novel.visibility.in_(["public", "seed"]))
    else:
        return query.where(Novel.visibility == "public")
```

### 7.3 API 接口

#### 7.3.1 用户角色管理

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| GET | `/api/admin/users` | admin | 获取所有用户列表 |
| PUT | `/api/admin/users/{id}/role` | admin | 修改用户角色 |
| GET | `/api/admin/users/search` | admin | 按用户名搜索 |

```
GET /api/admin/users?page=1&page_size=20
Response: {
  code: 0,
  data: {
    users: [
      { id, username, role, avatar, created_at },
      ...
    ],
    total: number
  }
}

PUT /api/admin/users/{id}/role
Body: { role: "seed_member" }
校验: 不能修改自己的角色（防止管理员误操作降级自己）
Response: { code: 0, message: "角色修改成功" }
```

#### 7.3.2 小说可见性管理

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| PUT | `/api/novels/{id}/visibility` | admin | 修改小说可见性 |
| GET | `/api/novels/{id}` | 需登录 | 增加可见性校验（无权返回 403） |

```
PUT /api/novels/{id}/visibility
Body: { visibility: "seed" }
Response: { code: 0, message: "可见性修改成功" }
```

#### 7.3.3 小说下载

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| GET | `/api/novels/{id}/download` | seed_member+ | 下载 TXT 原文件 |

```
GET /api/novels/{id}/download
权限: seed_member 或 admin
Response: 直接返回文件流（Content-Disposition: attachment）
```

#### 7.3.4 现有接口的改造

以下接口需要增加角色过滤：

| 接口 | 改动 |
|------|------|
| `GET /api/novels` | 按用户角色过滤可见性 |
| `GET /api/novels/hot` | 按用户角色过滤可见性 |
| `GET /api/novels/latest` | 按用户角色过滤可见性 |
| `GET /api/novels/search` | 按用户角色过滤可见性 |
| `GET /api/bookshelf` | 按用户角色过滤可见性 |
| `POST /api/upload/novel` | 限制只有 seed_member+ 可上传 |

### 7.4 后端改动清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `app/models/novel.py` | 修改 | 新增 `visibility` 字段 |
| `app/api/auth.py` | 修改 | 新增 `require_role`、`require_min_role`、`get_visible_novels_query` |
| `app/api/admin.py` | **新增** | 用户角色管理接口 |
| `app/api/novel.py` | 修改 | 新增下载/可见性接口；现有接口加过滤 |
| `app/schemas/novel.py` | 修改 | 新增 visibility 字段到 schema |
| `app/schemas/admin.py` | **新增** | 管理员接口 schema |
| `app/main.py` | 修改 | 注册 admin 路由 |

## 8. 前端实现

### 8.1 路由守卫增强

```typescript
// router/guards.ts 新增

// 角色检查函数（配合路由 meta 使用）
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();

  // 需要特定角色
  const requiredRole = to.meta.requiredRole as string | undefined;
  if (requiredRole) {
    const ROLE_LEVEL: Record<string, number> = { member: 0, seed_member: 1, admin: 2 };
    const userLevel = ROLE_LEVEL[userStore.user?.role || 'member'];
    const requiredLevel = ROLE_LEVEL[requiredRole];
    if (userLevel < requiredLevel) {
      return next({ name: 'Home' }); // 权限不足，回首页
    }
  }

  next();
});
```

### 8.2 前端权限工具函数

```typescript
// composables/usePermission.ts
export function usePermission() {
  const userStore = useUserStore()

  const isAdmin = computed(() => userStore.user?.role === 'admin')
  const isSeedMember = computed(() => userStore.user?.role === 'seed_member' || isAdmin.value)
  const isMember = computed(() => !!userStore.user)

  function canUpload() { return isSeedMember.value }
  function canDownload() { return isSeedMember.value }
  function canManageRoles() { return isAdmin.value }
  function canReadAnyNovel() { return isSeedMember.value }

  return { isAdmin, isSeedMember, isMember, canUpload, canDownload, canManageRoles, canReadAnyNovel }
}
```

### 8.3 上传页改造

- 上传按钮仅 `seed_member`+ 可见
- 普通成员访问 `/upload` 重定向到首页
- 上传时可选择小说可见性（仅 admin 有此选项）

### 8.4 用户管理页 AdminUsersView.vue

- 表格展示所有用户（用户名、角色、注册时间）
- 角色列使用 `el-select` 下拉切换
- 保存时调用 `PUT /api/admin/users/{id}/role`
- 搜索框支持按用户名过滤（前端过滤或调搜索接口）
- 路由配置 `meta: { requiredRole: 'admin' }`

### 8.5 前端改动清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `views/AdminUsersView.vue` | **新增** | 用户角色管理页 |
| `composables/usePermission.ts` | **新增** | 权限判断工具函数 |
| `router/index.ts` | 修改 | 新增 `/admin/users` 路由 + `requiredRole` meta |
| `router/guards.ts` | 修改 | 新增角色级别路由守卫 |
| `views/UploadView.vue` | 修改 | 上传按钮权限控制 + admin 可见性选择 |
| `views/LibraryView.vue` | 修改 | 按可见性过滤展示 |
| `services/admin.ts` | **新增** | 管理员 API 服务 |
| `services/novel.ts` | 修改 | 新增下载接口 |

## 9. 验收标准

- [ ] Novel 模型新增 `visibility` 字段（public / seed / admin）
- [ ] 上传小说默认 `public`，管理员可选择可见性
- [ ] 普通成员只能看到和阅读 `public` 小说
- [ ] 种子成员可看到 `public` + `seed` 小说
- [ ] 管理员可看到全部小说
- [ ] 种子成员+管理员可下载 TXT 原文件
- [ ] 普通成员只能阅读已加入书架的小说
- [ ] 仅有种子成员+管理员可上传小说
- [ ] 管理员用户管理页可查看所有用户列表
- [ ] 管理员可通过下拉框修改用户角色
- [ ] 管理员不能修改自己的角色（防锁死）
- [ ] 现有接口均按角色过滤返回内容
- [ ] 前端路由守卫按角色拦截无权限页面
- [ ] 未登录用户只能浏览公开内容，不能阅读

## 10. 依赖关系

```
REQ-P3-004 权限系统
├── 依赖 User 模型 role 字段（已存在）
├── 依赖 Novel 模型（需新增 visibility 字段）
├── 影响 REQ-P2-002 阅读器（需加入可见性检查）
├── 影响 REQ-P3-002 首页+搜索（需按角色过滤内容）
└── 与 REQ-P3-003 帮助页无直接依赖
```

> ⚠️ 本需求为基础设施，**建议优先开发**，后续阅读器和首页开发时直接依赖本需求的权限体系。

---

*本文件由 AI 在 2026-06-28 创建*

# 权限系统模块规范

> **优先级**: P0 - 必须遵守
> **最后更新**: 2026-06-28
> **覆盖范围**: 三级角色体系 + 三级可见性 + 前端权限判断 + 后端权限依赖

## 1. 权限模型

### 角色层级

```
admin (管理员)        level=2
  ↑ 继承
seed_member (种子成员)  level=1
  ↑ 继承
member (普通成员)       level=0
```

### 可见性层级

```
public   → 所有人可见（含未登录）
seed     → seed_member 及以上可见
admin    → 仅 admin 可见
```

## 2. 权限矩阵

| 操作 | member | seed_member | admin |
|------|--------|-------------|-------|
| 浏览 public 小说 | ✅ | ✅ | ✅ |
| 浏览 seed 小说 | ❌ | ✅ | ✅ |
| 浏览 admin 小说 | ❌ | ❌ | ✅ |
| 上传小说 | ❌ | ✅ | ✅ |
| 下载小说 | ❌ | ✅ | ✅ |
| 删除自己的小说 | ✅ | ✅ | ✅ |
| 删除他人小说 | ❌ | ❌ | ✅ |
| 修改可见性 | ❌ | ❌ | ✅ |
| 管理用户角色 | ❌ | ❌ | ✅ |
| 访问管理页 | ❌ | ❌ | ✅ |

## 3. 后端实现

### 权限依赖函数

```python
# app/api/auth.py

ROLE_LEVEL = {"member": 0, "seed_member": 1, "admin": 2}

def get_current_user(
    authorization: str = Header(None),
    session: Session = Depends(get_session)
) -> User:
    """从 JWT 解析当前用户，失败返回 401"""
    ...

def require_role(*allowed_roles: str):
    """精确角色匹配"""
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="无权限访问")
        return current_user
    return checker

def require_min_role(min_role: str):
    """最低角色级别"""
    min_level = ROLE_LEVEL[min_role]
    async def checker(current_user = Depends(get_current_user)):
        if ROLE_LEVEL.get(current_user.role, 0) < min_level:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user
    return checker
```

### 可见性过滤

```python
# app/api/novel.py

def _get_visible_query(current_user: Optional[User]):
    """根据用户角色构建可见性过滤条件"""
    if current_user is None:
        return Novel.visibility == "public"
    if current_user.role == "admin":
        return True  # 管理员看全部
    if current_user.role == "seed_member":
        return Novel.visibility.in_(["public", "seed"])
    return Novel.visibility == "public"  # member

# 列表接口使用
query = query.where(_get_visible_query(current_user))
```

## 4. 前端实现

### usePermission Composable

```typescript
// composables/usePermission.ts
export function usePermission() {
  const userStore = useUserStore();

  const isLoggedIn = computed(() => userStore.isAuthenticated);
  const isAdmin = computed(() => userStore.user?.role === 'admin');
  const isSeedMember = computed(() =>
    userStore.user?.role === 'seed_member' || userStore.user?.role === 'admin'
  );

  function canUpload(): boolean {
    return isSeedMember.value;
  }

  function canDownload(): boolean {
    return isSeedMember.value;
  }

  function canManageRoles(): boolean {
    return isAdmin.value;
  }

  function canViewNovel(novel: { visibility: string }): boolean {
    if (novel.visibility === 'public') return true;
    if (!isLoggedIn.value) return false;
    if (novel.visibility === 'seed') return isSeedMember.value;
    if (novel.visibility === 'admin') return isAdmin.value;
    return false;
  }

  return {
    isLoggedIn, isAdmin, isSeedMember,
    canUpload, canDownload, canManageRoles, canViewNovel,
  };
}
```

### 视图层使用

```vue
<script setup lang="ts">
const { canUpload, canManageRoles } = usePermission();
</script>

<template>
  <!-- 条件渲染 -->
  <el-button v-if="canUpload()" @click="showUpload">上传小说</el-button>
  <router-link v-if="canManageRoles()" to="/admin/users">用户管理</router-link>
</template>
```

### 路由守卫

```typescript
// router/index.ts
{
  path: '/admin/users',
  name: 'AdminUsers',
  component: () => import('@/views/AdminUsersView.vue'),
  meta: {
    requiresAuth: true,
    requiredRole: 'admin',   // 仅管理员
    title: '用户管理',
  },
}
```

```typescript
// router/guards.ts — role 检查
if (to.meta.requiredRole) {
  const roleLevel: Record<string, number> = {
    member: 0, seed_member: 1, admin: 2
  };
  if (roleLevel[userStore.user!.role] < roleLevel[to.meta.requiredRole]) {
    return next({ name: 'Home' });
  }
}
```

## 5. AdminUsersView 管理页

```
/admin/users
┌──────────────────────────────────────────┐
│  AppHeader                               │
├──────────────────────────────────────────┤
│  🔍 搜索用户...                          │
├──────┬──────────┬──────────┬─────────────┤
│ 用户  │ 角色      │ 注册时间   │ 操作        │
├──────┼──────────┼──────────┼─────────────┤
│ test │ 管理员    │ 2026-06  │ [角色下拉]   │
│ user │ 普通成员  │ 2026-06  │ [角色下拉]   │
└──────┴──────────┴──────────┴─────────────┘
```

- 列表分页展示所有用户
- 角色通过 `el-select` 下拉修改
- 禁止修改自己的角色
- 角色选项：`admin` / `seed_member` / `member`

## 6. 设计决策 ADR

> 详见 [[06_architecture-decisions]] ADR-001

**核心决策**: 权限采用**纯可见性控制**，书架不承担权限职责。

- 普通成员可直接阅读所有 `public` 小说（无需加入书架）
- 书架回归收藏夹本质
- 一层 `visibility` 字段完成内容分发

## 7. 验收清单

- [ ] 三级角色可创建（admin/seed_member/member）
- [ ] 小说上传时可设置可见性（public/seed/admin）
- [ ] 低角色无法看到高可见性小说
- [ ] 低角色上传/下载按钮隐藏
- [ ] 仅管理员可访问 `/admin/users`
- [ ] 管理员可修改他人角色
- [ ] 管理员不可修改自己角色
- [ ] 书架不限制阅读权限（public 小说无需加入书架即可阅读）

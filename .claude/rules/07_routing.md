# 07 — 路由规范

## 路由配置标准

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),  // ✅ 懒加载
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/views/LibraryView.vue'),
    meta: { requiresAuth: true, title: '我的书房' },
  },
  {
    path: '/reader/:id',
    name: 'Reader',
    component: () => import('@/views/ReaderView.vue'),
    props: true,  // 将路由参数作为 props 传入组件
    meta: { title: '阅读' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

## 路由守卫

```typescript
// router/guards.ts
import type { Router } from 'vue-router';
import { useUserStore } from '@/stores/user';

export function setupRouterGuards(router: Router) {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const requiresAuth = to.matched.some(r => r.meta.requiresAuth);

    if (requiresAuth && !userStore.isAuthenticated) {
      next({ name: 'Login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  });

  // 全局后置守卫：设置页面标题
  router.afterEach((to) => {
    const title = to.meta.title as string;
    document.title = title ? `${title} | 小说阅读平台` : '小说阅读平台';
  });
}
```

## Meta 字段约定

```typescript
// 路由 meta 字段使用声明
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;   // 是否需要登录
    title?: string;           // 页面标题
    hideNavbar?: boolean;     // 是否隐藏导航栏
    roles?: string[];         // 允许访问的角色
  }
}
```

## 命名规范

| 项目 | 命名方式 | 示例 |
|------|----------|------|
| 路由 `name` | PascalCase | `Home`, `NovelDetail` |
| 路由 `path` | kebab-case | `/novel-list`, `/reader/:id` |
| 视图文件 | `*View.vue` | `HomeView.vue`, `LibraryView.vue` |

## ✅ 规则速查

- ✅ 所有页面组件**必须懒加载**（`() => import(...)`）
- ✅ 需要认证的路由设置 `meta.requiresAuth = true`
- ✅ 传递路由参数优先使用 `props: true`
- ✅ 登录后重定向回原页面（通过 `redirect` query 参数）
- ❌ 禁止直接导入视图组件（破坏代码分割）

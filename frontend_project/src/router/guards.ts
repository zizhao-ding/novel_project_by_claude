import type { Router } from 'vue-router';
import { useUserStore } from '../stores/user';

export function setupRouterGuards(router: Router) {
  // 全局前置守卫：鉴权检查
  router.beforeEach((to, _from, next) => {
    const userStore = useUserStore();
    const requiresAuth = to.matched.some((r) => r.meta.requiresAuth);

    if (requiresAuth && !userStore.isAuthenticated) {
      // 未登录，跳转登录页并记录目标路径
      next({ name: 'Login', query: { redirect: to.fullPath } });
      return;
    }
    if ((to.name === 'Login' || to.name === 'Register') && userStore.isAuthenticated) {
      // 已登录用户访问登录/注册页，重定向到首页
      next({ name: 'Home' });
      return;
    }
    // 角色检查
    const requiredRole = to.meta.requiredRole as string | undefined;
    if (requiredRole) {
      const ROLE_LEVEL: Record<string, number> = { member: 0, seed_member: 1, admin: 2 };
      const userLevel = ROLE_LEVEL[userStore.user?.role || 'member'] ?? 0;
      const requiredLevel = ROLE_LEVEL[requiredRole] ?? 0;
      if (userLevel < requiredLevel) {
        next({ name: 'Home' });
        return;
      }
    }
    next();
  });

  // 全局后置守卫：设置页面标题
  router.afterEach((to) => {
    const title = to.meta.title as string | undefined;
    // eslint-disable-next-line no-restricted-globals -- 设置页面标题需要直接操作 document
    document.title = title ? `${title} | 小说阅读平台` : '小说阅读平台';
  });
}

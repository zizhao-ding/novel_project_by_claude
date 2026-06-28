import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { setupRouterGuards } from './guards';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '首页' },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { title: '注册' },
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('../views/LibraryView.vue'),
    meta: { requiresAuth: true, title: '我的书房' },
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('../views/UploadView.vue'),
    meta: { requiresAuth: true, title: '上传小说' },
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('../views/UserView.vue'),
    meta: { requiresAuth: true, title: '我的' },
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/AdminUsersView.vue'),
    meta: { requiresAuth: true, requiredRole: 'admin', title: '用户管理' },
  },
  {
    path: '/reader/:id',
    name: 'Reader',
    component: () => import('../views/ReaderView.vue'),
    props: true,
    meta: { title: '阅读' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
    meta: { title: '页面不存在' },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// 注册路由守卫
setupRouterGuards(router);

export default router;

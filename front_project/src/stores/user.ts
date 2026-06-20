import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '../types/user';
import { authApi } from '../services/auth';
import { sha256 } from '../utils/crypto';

export const useUserStore = defineStore('user', () => {
  // ── State ──
  const user = ref<User | null>(null);
  const token = ref<string | null>(localStorage.getItem('token'));
  const loading = ref(false);
  const error = ref<string | null>(null);

  // ── Getters ──
  const isAuthenticated = computed(() => !!token.value);

  // ── Actions ──
  /**
   * 用户注册
   * 注册成功后跳转登录页
   */
  async function register(username: string, password: string) {
    loading.value = true;
    error.value = null;
    try {
      // 前端 SHA256 哈希后发送
      const hashedPassword = sha256(password);
      const res = await authApi.register({ username, password: hashedPassword });

      if (res.code === 0) {
        ElMessage.success('注册成功，请登录');
        return true;
      } else {
        error.value = res.message;
        ElMessage.error(res.message || '注册失败');
        return false;
      }
    } catch (err) {
      const msg = (err as Error).message || '网络请求失败';
      error.value = msg;
      ElMessage.error(msg);
      return false;
    } finally {
      loading.value = false;
    }
  }

  /**
   * 用户登录
   * 登录成功存储 token 并获取用户信息
   */
  async function login(username: string, password: string) {
    loading.value = true;
    error.value = null;
    try {
      const hashedPassword = sha256(password);
      const res = await authApi.login({ username, password: hashedPassword });

      if (res.code === 0 && res.data) {
        token.value = res.data.token;
        user.value = res.data.user;
        localStorage.setItem('token', res.data.token);
        ElMessage.success('登录成功');
        return true;
      } else {
        error.value = res.message;
        ElMessage.error(res.message || '用户名或密码错误');
        return false;
      }
    } catch (err) {
      const msg = '登录失败，请检查网络连接';
      error.value = msg;
      ElMessage.error(msg);
      return false;
    } finally {
      loading.value = false;
    }
  }

  /**
   * 退出登录
   */
  function logout() {
    user.value = null;
    token.value = null;
    localStorage.removeItem('token');
    ElMessage.success('已退出登录');
  }

  /**
   * 获取当前用户信息
   * 用于页面刷新后恢复登录状态
   */
  async function fetchProfile() {
    if (!token.value) return;
    try {
      const res = await authApi.getProfile();
      if (res.code === 0 && res.data) {
        user.value = res.data;
      } else {
        // token 无效，清除
        logout();
      }
    } catch {
      // profile 接口暂未实现时，保留 token
    }
  }

  /**
   * 清除错误信息
   */
  function clearError() {
    error.value = null;
  }

  return {
    // State
    user, token, loading, error,
    // Getters
    isAuthenticated,
    // Actions
    register, login, logout, fetchProfile, clearError,
  };
});

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '../user';
import type { User } from '../../types/user';

// 使用 vi.hoisted 确保 mock 数据在 mock 调用前可用
const mockUser = vi.hoisted<User>(() => ({
  id: 1,
  username: 'testuser',
  role: 'member',
  avatar: '#F5A623',
  created_at: '2026-01-01T00:00:00Z',
}));

// Mock Element Plus modules
vi.mock('element-plus', () => ({
  ElMessage: { success: vi.fn(), error: vi.fn(), warning: vi.fn(), info: vi.fn() },
  ElMessageBox: { confirm: vi.fn(() => Promise.resolve('confirm')) },
}));

// Mock auth service
vi.mock('@/services/auth', () => ({
  authApi: {
    login: vi.fn().mockResolvedValue({
      code: 0,
      data: { token: 'test-token', user: mockUser },
    }),
    register: vi.fn().mockResolvedValue({ code: 0 }),
    getProfile: vi.fn().mockResolvedValue({ code: 0, data: mockUser }),
    getUserStats: vi.fn().mockResolvedValue({ code: 0, data: {} }),
  },
}));

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(() => null),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
// eslint-disable-next-line no-restricted-globals -- 测试环境需要访问 window
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

describe('useUserStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  it('初始状态应该为空', () => {
    const store = useUserStore();
    expect(store.user).toBeNull();
    expect(store.token).toBeNull();
    expect(store.isAuthenticated).toBe(false);
  });

  it('login 应该设置 token 和 user', async () => {
    const store = useUserStore();

    await store.login('testuser', 'password123');

    expect(store.token).toBe('test-token');
    expect(store.user).toEqual(mockUser);
    expect(store.isAuthenticated).toBe(true);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'test-token');
  });

  it('logout 应该清除状态', async () => {
    const store = useUserStore();
    store.token = 'test-token';
    store.user = mockUser;

    await store.logout();

    expect(store.token).toBeNull();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
  });

  it('fetchProfile 应该获取用户信息', async () => {
    const store = useUserStore();
    store.token = 'test-token';

    await store.fetchProfile();

    expect(store.user).toEqual(mockUser);
  });
});

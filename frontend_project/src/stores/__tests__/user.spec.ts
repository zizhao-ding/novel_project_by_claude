import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '../user';

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
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
    const mockResponse = {
      code: 0,
      data: {
        token: 'test-token',
        user: { id: 1, username: 'testuser' },
      },
    };

    // Mock API call
    vi.mock('@/services/auth', () => ({
      authApi: {
        login: vi.fn().mockResolvedValue(mockResponse),
      },
    }));

    await store.login('testuser', 'password123');

    expect(store.token).toBe('test-token');
    expect(store.user).toEqual({ id: 1, username: 'testuser' });
    expect(store.isAuthenticated).toBe(true);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'test-token');
  });

  it('logout 应该清除状态', () => {
    const store = useUserStore();
    store.token = 'test-token';
    store.user = { id: 1, username: 'testuser' };

    store.logout();

    expect(store.token).toBeNull();
    expect(store.user).toBeNull();
    expect(store.isAuthenticated).toBe(false);
    expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
  });

  it('fetchProfile 应该获取用户信息', async () => {
    const store = useUserStore();
    store.token = 'test-token';

    const mockUser = { id: 1, username: 'testuser' };

    // Mock API call
    vi.mock('@/services/auth', () => ({
      authApi: {
        getProfile: vi.fn().mockResolvedValue({ code: 0, data: mockUser }),
      },
    }));

    await store.fetchProfile();

    expect(store.user).toEqual(mockUser);
  });
});

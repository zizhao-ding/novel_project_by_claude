import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useNovelStore } from '../novel';

// Mock data — vi.hoisted ensures they are available inside vi.mock factories
const mockNovel = vi.hoisted(() => ({
  id: 1,
  title: '测试小说',
  user_id: 1,
  username: 'testuser',
  file_path: '/uploads/novels/test.txt',
  file_size: 102400,
  category_id: null,
  visibility: 'public' as const,
  created_at: '2026-06-01T00:00:00Z',
  updated_at: '2026-06-01T00:00:00Z',
}));

const mockNovel2 = vi.hoisted(() => ({
  id: 2,
  title: '第二本小说',
  user_id: 1,
  username: 'testuser',
  file_path: '/uploads/novels/test2.txt',
  file_size: 204800,
  category_id: 1,
  visibility: 'public' as const,
  created_at: '2026-06-02T00:00:00Z',
  updated_at: '2026-06-02T00:00:00Z',
}));

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: { success: vi.fn(), error: vi.fn(), warning: vi.fn(), info: vi.fn() },
  ElMessageBox: { confirm: vi.fn(() => Promise.resolve('confirm')) },
}));

// Mock novel API — 所有 mock 函数在工厂内创建
vi.mock('@/services/novel', () => ({
  novelApi: {
    getList: vi.fn().mockResolvedValue({
      code: 0,
      data: { items: [mockNovel, mockNovel2], total: 2 },
    }),
    upload: vi.fn().mockResolvedValue({
      code: 0,
      message: '上传成功',
      data: mockNovel,
    }),
    delete: vi.fn().mockResolvedValue({ code: 0 }),
  },
}));

// 延迟导入 mock 模块（vi.mock 已生效）
import { novelApi } from '@/services/novel';

describe('useNovelStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  describe('初始状态', () => {
    it('状态应为空', () => {
      const store = useNovelStore();
      expect(store.novels).toEqual([]);
      expect(store.loading).toBe(false);
      expect(store.uploading).toBe(false);
      expect(store.uploadProgress).toBe(0);
      expect(store.error).toBeNull();
    });
  });

  describe('fetchNovels', () => {
    it('应加载小说列表', async () => {
      const store = useNovelStore();
      await store.fetchNovels();

      expect(store.novels).toHaveLength(2);
      expect(store.novels[0].title).toBe('测试小说');
      expect(store.loading).toBe(false);
    });

    it('加载中应设置 loading=true', async () => {
      const store = useNovelStore();
      vi.mocked(novelApi.getList).mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({ code: 0, data: { items: [], total: 0 } }), 50))
      );

      const promise = store.fetchNovels();
      expect(store.loading).toBe(true);

      await promise;
      expect(store.loading).toBe(false);
    });

    it('API 失败时应设置 error', async () => {
      const store = useNovelStore();
      vi.mocked(novelApi.getList).mockRejectedValueOnce(new Error('网络错误'));

      await store.fetchNovels();

      expect(store.error).toBe('网络错误');
      expect(store.loading).toBe(false);
    });
  });

  describe('deleteNovel', () => {
    it('应从列表中移除已删除的小说', async () => {
      const store = useNovelStore();
      await store.fetchNovels();
      expect(store.novels).toHaveLength(2);

      await store.deleteNovel(1);

      expect(store.novels).toHaveLength(1);
      expect(store.novels[0].id).toBe(2);
    });

    it('删除失败时列表不应变化', async () => {
      const store = useNovelStore();
      await store.fetchNovels();
      vi.mocked(novelApi.delete).mockRejectedValueOnce(new Error('删除失败'));

      await store.deleteNovel(1);

      expect(store.novels).toHaveLength(2);
    });
  });

  describe('uploadNovel', () => {
    it('上传成功应添加到列表头部', async () => {
      const store = useNovelStore();

      const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
      const result = await store.uploadNovel(file);

      expect(result).toBe(true);
      expect(store.novels[0].title).toBe('测试小说');
    });

    it('上传中应设置 uploading=true', async () => {
      const store = useNovelStore();
      vi.mocked(novelApi.upload).mockImplementationOnce(
        () => new Promise(resolve => setTimeout(() => resolve({ code: 0, data: mockNovel }), 50))
      );

      const file = new File(['test'], 'test.txt', { type: 'text/plain' });
      const promise = store.uploadNovel(file);

      expect(store.uploading).toBe(true);

      await promise;
      expect(store.uploading).toBe(false);
    });

    it('上传失败应返回 false', async () => {
      const store = useNovelStore();
      vi.mocked(novelApi.upload).mockResolvedValueOnce({ code: 400, message: '上传失败' });

      const file = new File(['test'], 'test.txt', { type: 'text/plain' });
      const result = await store.uploadNovel(file);

      expect(result).toBe(false);
    });
  });
});

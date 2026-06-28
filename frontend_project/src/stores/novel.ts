import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { Novel, NovelListData } from '../types/novel';
import type { ApiResponse } from '../types/user';
import { novelApi } from '../services/novel';

export const useNovelStore = defineStore('novel', () => {
  const novels = ref<Novel[]>([]);
  const uploading = ref(false);
  const uploadProgress = ref(0);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function uploadNovel(file: File) {
    uploading.value = true;
    uploadProgress.value = 0;
    error.value = null;
    try {
      const onProgress = (pct: number) => {
        uploadProgress.value = pct;
      };
      const response = await novelApi.upload(file, onProgress);
      const res = response as unknown as ApiResponse<Novel>;
      if (res.code === 0 && res.data) {
        novels.value.unshift(res.data);
        ElMessage.success('上传成功');
        return true;
      } else {
        error.value = res.message;
        ElMessage.error(res.message || '上传失败');
        return false;
      }
    } catch {
      const msg = '上传失败，请检查网络连接';
      error.value = msg;
      ElMessage.error(msg);
      return false;
    } finally {
      uploading.value = false;
      uploadProgress.value = 0;
    }
  }

  async function fetchNovels() {
    loading.value = true;
    error.value = null;
    try {
      const response = await novelApi.getList();
      const res = response as unknown as { code: number; data: NovelListData };
      if (res.code === 0 && res.data) {
        novels.value = res.data.items;
      }
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  /** 删除小说（纯操作，确认弹窗由调用方负责） */
  async function deleteNovel(id: number) {
    try {
      await novelApi.delete(id);
      novels.value = novels.value.filter((n) => n.id !== id);
      ElMessage.success('删除成功');
    } catch {
      ElMessage.error('删除失败');
    }
  }

  return { novels, uploading, uploadProgress, loading, error, uploadNovel, fetchNovels, deleteNovel };
});

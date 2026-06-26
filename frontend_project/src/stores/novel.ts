import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import type { Novel } from '../types/novel';
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
      const res = await novelApi.upload(file, onProgress);
      if (res.code === 0 && res.data) {
        novels.value.unshift(res.data);
        ElMessage.success('上传成功');
        return true;
      } else {
        error.value = res.message;
        ElMessage.error(res.message || '上传失败');
        return false;
      }
    } catch (err) {
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
      const res = await novelApi.getList();
      if (res.code === 0 && res.data) {
        novels.value = res.data.items;
      }
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  async function deleteNovel(id: number) {
    try {
      await ElMessageBox.confirm('删除后不可恢复，确定要删除吗？', '确认删除', {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      });
      await novelApi.delete(id);
      novels.value = novels.value.filter((n) => n.id !== id);
      ElMessage.success('删除成功');
    } catch {
      // 用户取消
    }
  }

  return { novels, uploading, uploadProgress, loading, error, uploadNovel, fetchNovels, deleteNovel };
});

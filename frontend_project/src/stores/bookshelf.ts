import { defineStore } from 'pinia';
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
import type { BookshelfNovel } from '../types/bookshelf';
import { bookshelfApi } from '../services/bookshelf';

export const useBookshelfStore = defineStore('bookshelf', () => {
  // ── State ──
  const books = ref<BookshelfNovel[]>([]);
  const loading = ref(false);

  // ── Actions ──

  /** 获取书架列表 */
  async function fetchBooks() {
    loading.value = true;
    try {
      const res = await bookshelfApi.getList();
      if (res.code === 0 && res.data) {
        books.value = res.data.items;
      }
    } catch (err) {
      console.error('获取书架列表失败:', err);
    } finally {
      loading.value = false;
    }
  }

  /** 从书架移除 */
  async function removeBook(novelId: number) {
    try {
      const res = await bookshelfApi.remove(novelId);
      if (res.code === 0) {
        books.value = books.value.filter((b) => b.novel_id !== novelId);
        ElMessage.success('已从书架移除');
      } else {
        ElMessage.error(res.message || '移除失败');
      }
    } catch {
      ElMessage.error('移除失败');
    }
  }

  /** 批量从书架移除 */
  async function batchRemoveBooks(novelIds: number[]) {
    try {
      const res = await bookshelfApi.batchRemove(novelIds);
      if (res.code === 0) {
        books.value = books.value.filter((b) => !novelIds.includes(b.novel_id));
        ElMessage.success(res.message || '移除成功');
        return true;
      } else {
        ElMessage.error(res.message || '移除失败');
        return false;
      }
    } catch {
      ElMessage.error('移除失败');
      return false;
    }
  }

  return {
    books,
    loading,
    fetchBooks,
    removeBook,
    batchRemoveBooks,
  };
});

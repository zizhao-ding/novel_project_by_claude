import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import type { Category, CategoryListData, BatchCategoryRequest } from '../types/category';
import type { ApiResponse } from '../types/user';
import { categoryApi } from '../services/category';

/** 预设分类颜色 */
const PRESET_COLORS = [
  '#e74c3c',
  '#e67e22',
  '#f1c40f',
  '#2ecc71',
  '#1abc9c',
  '#3498db',
  '#9b59b6',
  '#34495e',
  '#e84393',
  '#00b894',
  '#0984e3',
  '#6c5ce7',
];

export const useCategoryStore = defineStore('category', () => {
  // ── State ──
  const categories = ref<Category[]>([]);
  const loading = ref(false);

  // ── Getters ──
  const categoryMap = computed(() => {
    const map = new Map<number, Category>();
    for (const cat of categories.value) {
      map.set(cat.id, cat);
    }
    return map;
  });

  // ── Actions ──

  /** 获取分类列表 */
  async function fetchCategories() {
    loading.value = true;
    try {
      const response = await categoryApi.getList();
      const res = response as unknown as { code: number; data: CategoryListData };
      if (res.code === 0 && res.data) {
        categories.value = res.data.items;
      }
    } catch {
      // 获取分类列表失败，静默处理
    } finally {
      loading.value = false;
    }
  }

  /** 创建分类 */
  async function createCategory(name: string, color?: string): Promise<boolean> {
    try {
      const colorIndex = categories.value.length % PRESET_COLORS.length;
      const assignedColor = color || PRESET_COLORS[colorIndex] || '#3498db';
      const response = await categoryApi.create({ name, color: assignedColor });
      const res = response as unknown as ApiResponse<Category>;
      if (res.code === 0 && res.data) {
        categories.value.push(res.data);
        ElMessage.success(`分类「${name}」创建成功`);
        return true;
      } else {
        ElMessage.error(res.message || '创建失败');
        return false;
      }
    } catch {
      ElMessage.error('创建分类失败');
      return false;
    }
  }

  /** 删除分类 */
  async function deleteCategory(id: number) {
    try {
      const response = await categoryApi.delete(id);
      const res = response as unknown as { code: number; message: string };
      if (res.code === 0) {
        categories.value = categories.value.filter((c) => c.id !== id);
        ElMessage.success('分类已删除');
      } else {
        ElMessage.error(res.message || '删除失败');
      }
    } catch {
      ElMessage.error('删除分类失败');
    }
  }

  /** 批量修改小说分类 */
  async function batchUpdateCategory(novelIds: number[], categoryId: number | null): Promise<boolean> {
    try {
      const data: BatchCategoryRequest = { novel_ids: novelIds, category_id: categoryId };
      const response = await categoryApi.batchUpdate(data);
      const res = response as unknown as { code: number; message: string };
      if (res.code === 0) {
        ElMessage.success(res.message || '分类修改成功');
        return true;
      } else {
        ElMessage.error(res.message || '修改失败');
        return false;
      }
    } catch {
      ElMessage.error('修改分类失败');
      return false;
    }
  }

  /** 获取随机预设颜色 */
  function getNextColor(): string {
    return PRESET_COLORS[categories.value.length % PRESET_COLORS.length] || '#3498db';
  }

  return {
    categories,
    loading,
    categoryMap,
    fetchCategories,
    createCategory,
    deleteCategory,
    batchUpdateCategory,
    getNextColor,
  };
});

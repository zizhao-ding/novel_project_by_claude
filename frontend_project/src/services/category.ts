import { api } from './api';
import type { ApiResponse } from '../types/user';
import type { Category, CategoryListData, BatchCategoryRequest } from '../types/category';

export const categoryApi = {
  /** 获取分类列表 */
  getList: () => api.client.get<{ code: number; data: CategoryListData }>('/categories'),

  /** 创建分类 */
  create: (data: { name: string; color: string }) => api.client.post<ApiResponse<Category>>('/categories', data),

  /** 更新分类 */
  update: (id: number, data: { name?: string; color?: string }) => api.client.put<ApiResponse<Category>>(`/categories/${id}`, data),

  /** 删除分类 */
  delete: (id: number) => api.client.delete(`/categories/${id}`),

  /** 批量修改小说分类 */
  batchUpdate: (data: BatchCategoryRequest) =>
    api.client.put<{ code: number; message: string; data: { updated: number } | null }>('/novels/batch-category', data),
};

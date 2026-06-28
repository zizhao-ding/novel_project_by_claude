import { api } from './api';
import type { ApiResponse } from '../types/user';
import type { Novel, NovelListData } from '../types/novel';

export const novelApi = {
  upload: (file: File, onProgress?: (pct: number) => void, visibility = 'public') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('visibility', visibility);
    return api.client.post<ApiResponse<Novel>>('/upload/novel', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (e.total && onProgress) {
          onProgress(Math.round((e.loaded * 100) / e.total));
        }
      },
    });
  },

  getList: (page = 1, pageSize = 20) =>
    api.client.get<{ code: number; data: NovelListData }>('/novels', {
      params: { page, page_size: pageSize },
    }),

  delete: (id: number) => api.client.delete<ApiResponse<void>>(`/novels/${id}`),

  updateVisibility: (id: number, visibility: string) =>
    api.client.put<ApiResponse<void>>(`/novels/${id}/visibility`, { visibility }),
};

import { api } from './api';
import type { BookshelfListData } from '../types/bookshelf';

export const bookshelfApi = {
  /** 获取书架列表 */
  getList: () =>
    api.client.get<{ code: number; message: string; data: BookshelfListData }>('/bookshelf'),

  /** 加入书架 */
  add: (novelId: number) =>
    api.client.post<{ code: number; message: string }>('/bookshelf', { novel_id: novelId }),

  /** 从书架移除 */
  remove: (novelId: number) =>
    api.client.delete<{ code: number; message: string }>(`/bookshelf/${novelId}`),

  /** 批量从书架移除 */
  batchRemove: (novelIds: number[]) =>
    api.client.delete<{ code: number; message: string }>('/bookshelf', {
      params: { novel_ids: novelIds.join(',') },
    }),
};

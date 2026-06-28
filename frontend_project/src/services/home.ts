import { api } from './api';

interface HotNovelItem {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  category_name: string | null;
  visibility: string;
  bookshelf_count: number;
  created_at: string;
}

interface NovelItem {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  visibility: string;
  created_at: string;
}

export const homeApi = {
  getHotNovels: (limit = 10) =>
    api.client.get<{ code: number; data: { items: HotNovelItem[]; total: number } }>('/novels/hot', { params: { limit } }),

  getLatestNovels: (limit = 10, offset = 0) =>
    api.client.get<{ code: number; data: { items: NovelItem[]; total: number } }>('/novels/latest', { params: { limit, offset } }),
};

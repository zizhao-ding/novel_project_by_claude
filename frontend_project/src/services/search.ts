import { api } from './api';

interface SearchResultItem {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  category_name: string | null;
  visibility: string;
  created_at: string;
}

export const searchApi = {
  search: (keyword: string, page = 1, pageSize = 20) =>
    api.client.get<{ code: number; data: { items: SearchResultItem[]; total: number; page: number; page_size: number } }>(
      '/novels/search',
      {
        params: { keyword, page, page_size: pageSize },
      },
    ),
};

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { homeApi } from '../services/home';

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

export const useHomeStore = defineStore('home', () => {
  const hotNovels = ref<HotNovelItem[]>([]);
  const latestNovels = ref<NovelItem[]>([]);
  const loading = ref(false);

  async function fetchHotNovels() {
    try {
      const response = await homeApi.getHotNovels(10);
      const res = response as unknown as { code: number; data: { items: HotNovelItem[]; total: number } };
      if (res.code === 0 && res.data) {
        hotNovels.value = res.data.items;
      }
    } catch {
      // 静默
    }
  }

  async function fetchLatestNovels() {
    try {
      const response = await homeApi.getLatestNovels(10, 0);
      const res = response as unknown as { code: number; data: { items: NovelItem[]; total: number } };
      if (res.code === 0 && res.data) {
        latestNovels.value = res.data.items;
      }
    } catch {
      // 静默
    }
  }

  async function fetchAll() {
    loading.value = true;
    await Promise.all([fetchHotNovels(), fetchLatestNovels()]);
    loading.value = false;
  }

  return { hotNovels, latestNovels, loading, fetchHotNovels, fetchLatestNovels, fetchAll };
});

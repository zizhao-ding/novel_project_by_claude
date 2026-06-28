import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import { ElMessage } from 'element-plus';
import { readerApi } from '../services/reader';

interface ChapterInfo {
  index: number;
  title: string;
  start_pos: number;
  length: number;
}

interface ReadingProgress {
  chapter_index: number;
  scroll_percent: number;
  updated_at: string;
}

export const useReaderStore = defineStore('reader', () => {
  const novelId = ref<number>(0);
  const novelTitle = ref('');
  const chapters = ref<ChapterInfo[]>([]);
  const currentChapterIndex = ref(0);
  const currentContent = ref('');
  const currentTitle = ref('');
  const loading = ref(false);
  const sidebarVisible = ref(false);

  // 阅读设置（本地存储）
  const settings = useLocalStorage('reader-settings', {
    fontSize: 16,
    theme: 'light' as 'light' | 'dark' | 'sepia',
    lineHeight: 1.8,
  });

  // 阅读进度（远程）
  const progress = ref<ReadingProgress | null>(null);

  async function loadNovel(id: number, title: string) {
    // 切换小说时清空旧数据
    novelId.value = id;
    novelTitle.value = title;
    chapters.value = [];
    currentChapterIndex.value = 0;
    currentContent.value = '';
    currentTitle.value = '';
    progress.value = null;
    loading.value = true;
    try {
      const response = await readerApi.getChapters(id);
      const res = response as unknown as { code: number; data: { novel_id: number; chapters: ChapterInfo[] } };
      if (res.code === 0 && res.data) {
        chapters.value = res.data.chapters;
      }
      // 尝试恢复进度
      const pResp = await readerApi.getProgress(id);
      const pRes = pResp as unknown as { code: number; data: ReadingProgress | null };
      if (pRes.code === 0 && pRes.data) {
        progress.value = pRes.data;
        await loadChapter(pRes.data.chapter_index);
        // 如果进度显示用户看到了一半左右，提示恢复
        if (pRes.data.scroll_percent > 0 && pRes.data.scroll_percent < 90) {
          ElMessage.info(`已恢复到上次阅读位置（${Math.round(pRes.data.scroll_percent)}%）`);
        }
      } else {
        await loadChapter(0);
      }
    } catch {
      ElMessage.error('加载小说失败');
    } finally {
      loading.value = false;
    }
  }

  async function loadChapter(index: number) {
    if (index < 0 || index >= chapters.value.length) return;
    loading.value = true;
    try {
      const response = await readerApi.getChapterContent(novelId.value, index);
      const res = response as unknown as {
        code: number;
        data: { index: number; title: string; content: string; prev_index: number | null; next_index: number | null };
      };
      if (res.code === 0 && res.data) {
        currentChapterIndex.value = res.data.index;
        currentTitle.value = res.data.title;
        currentContent.value = res.data.content;
      }
    } catch {
      ElMessage.error('加载章节失败');
    } finally {
      loading.value = false;
    }
  }

  async function goToChapter(index: number) {
    await loadChapter(index);
    await saveProgress(index, 0);
    sidebarVisible.value = false;
  }

  async function goToNext() {
    const nextIdx = currentChapterIndex.value + 1;
    if (nextIdx < chapters.value.length) {
      await loadChapter(nextIdx);
      await saveProgress(nextIdx, 0);
    }
  }

  async function goToPrev() {
    const prevIdx = currentChapterIndex.value - 1;
    if (prevIdx >= 0) {
      await loadChapter(prevIdx);
      await saveProgress(prevIdx, 0);
    }
  }

  async function saveProgress(index?: number, scrollPercent?: number) {
    const idx = index ?? currentChapterIndex.value;
    const pct = scrollPercent ?? 0;
    try {
      await readerApi.saveProgress(novelId.value, idx, pct);
    } catch {
      // 静默失败，不影响阅读体验
    }
  }

  function toggleSidebar() {
    sidebarVisible.value = !sidebarVisible.value;
  }

  function setFontSize(delta: number) {
    const newSize = settings.value.fontSize + delta;
    if (newSize >= 12 && newSize <= 24) {
      settings.value.fontSize = newSize;
    }
  }

  function setTheme(theme: 'light' | 'dark' | 'sepia') {
    settings.value.theme = theme;
  }

  return {
    novelId,
    novelTitle,
    chapters,
    currentChapterIndex,
    currentContent,
    currentTitle,
    loading,
    sidebarVisible,
    settings,
    progress,
    loadNovel,
    loadChapter,
    goToChapter,
    goToNext,
    goToPrev,
    saveProgress,
    toggleSidebar,
    setFontSize,
    setTheme,
  };
});

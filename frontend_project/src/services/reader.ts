import { api } from './api';

interface ChapterInfo {
  index: number;
  title: string;
  start_pos: number;
  length: number;
}

interface ChapterContent {
  index: number;
  title: string;
  content: string;
  prev_index: number | null;
  next_index: number | null;
}

interface ReadingProgress {
  chapter_index: number;
  scroll_percent: number;
  updated_at: string;
}

export const readerApi = {
  /** 获取章节目录 */
  getChapters: (novelId: number) =>
    api.client.get<{ code: number; data: { novel_id: number; chapters: ChapterInfo[] } }>(`/novels/${novelId}/chapters`),

  /** 获取章节正文 */
  getChapterContent: (novelId: number, index: number) =>
    api.client.get<{ code: number; data: ChapterContent }>(`/novels/${novelId}/chapters/${index}`),

  /** 获取阅读进度 */
  getProgress: (novelId: number) => api.client.get<{ code: number; data: ReadingProgress | null }>(`/novels/${novelId}/progress`),

  /** 保存阅读进度 */
  saveProgress: (novelId: number, chapterIndex: number, scrollPercent: number) =>
    api.client.post<{ code: number; message: string }>(`/novels/${novelId}/progress`, {
      chapter_index: chapterIndex,
      scroll_percent: scrollPercent,
    }),
};

/** 书架中的小说 */
export interface BookshelfNovel {
  id: number;
  novel_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  added_at: string;
}

/** 书架列表数据 */
export interface BookshelfListData {
  items: BookshelfNovel[];
  total: number;
}

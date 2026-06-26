export interface Novel {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  created_at: string;
}

export interface NovelListData {
  items: Novel[];
  total: number;
}

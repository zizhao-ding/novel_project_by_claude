export interface Novel {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  visibility: 'public' | 'seed' | 'admin';
  username?: string;
  created_at: string;
}

/** 可见性配置 */
export const VISIBILITY_LABELS: Record<string, string> = {
  public: '公开',
  seed: '种子成员',
  admin: '仅管理',
};

export const VISIBILITY_COLORS: Record<string, string> = {
  public: 'success',
  seed: 'warning',
  admin: 'danger',
};

export const VISIBILITY_OPTIONS = [
  { value: 'public', label: '公开 — 所有人可见' },
  { value: 'seed', label: '种子成员 — 种子成员及以上可见' },
  { value: 'admin', label: '仅管理 — 仅管理员可见' },
];

export interface NovelListData {
  items: Novel[];
  total: number;
}

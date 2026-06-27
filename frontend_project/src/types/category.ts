/** 分类信息 */
export interface Category {
  id: number;
  user_id: number;
  name: string;
  color: string;
  created_at: string;
}

/** 分类列表数据 */
export interface CategoryListData {
  items: Category[];
  total: number;
}

/** 批量修改分类请求 */
export interface BatchCategoryRequest {
  novel_ids: number[];
  category_id: number | null;
}

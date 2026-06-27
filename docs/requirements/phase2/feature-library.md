# REQ-P2-001: 书房页面

> **状态**: ✅ done
> **优先级**: P1
> **创建日期**: 2026-06-27
> **最后更新**: 2026-06-27

## 1. 概述

实现书房页面（LibraryView.vue），作为用户的个人书架，展示用户收藏的小说。支持右侧分类栏筛选、长按多选批量管理（分类、删除），书架数据与用户绑定。

## 2. 用户故事

- 作为 **用户**，我想要 **查看我的书架上所有书籍**，以便 **快速找到想读的小说**
- 作为 **用户**，我想要 **通过右侧分类栏筛选书籍**，以便 **按类别浏览**
- 作为 **用户**，我想要 **创建自定义分类**，以便 **个性化整理书架**
- 作为 **用户**，我想要 **长按书籍进入多选模式**，以便 **批量管理书籍**
- 作为 **用户**，我想要 **对选中的书籍进行分类或删除**，以便 **整理我的书架**
- 作为 **用户**，我想要 **删除前弹窗确认**，以便 **防止误删**
- 作为 **用户**，我想要 **书架只显示我加入的书籍**，以便 **个人专属体验**

## 3. UI 布局

```
┌──────────────────────────────────────────────────┐
│ ← 我的书房                             [头像]    │  ← 顶部栏（头像可跳转用户页）
├──────────────────────────────────────┬───────────┤
│ 共 6 本书              [管理书架]    │  分类     │
├──────────────────────────────────────┤  ● 全部   │
│ ┌──────┐ ┌──────┐ ┌──────┐          │  ● 玄幻   │
│ │ 封面 │ │ 封面 │ │ 封面 │          │  ● 仙侠   │
│ │      │ │      │ │      │          │  ● 奇幻   │
│ ├──────┤ ├──────┤ ├──────┤          │  ● 游戏   │
│ │书名  │ │书名  │ │书名  │          │  + 新建   │
│ │大小  │ │大小  │ │大小  │          │           │
│ └──────┘ └──────┘ └──────┘          │           │
├──────────────────────────────────────┴───────────┤
│ 已选择 2 本书                     [分类] [删除]  │  ← 多选操作栏
└──────────────────────────────────────────────────┘
```

## 4. 路由 & 页面

- **路由**: `/library`
- **页面**: `LibraryView.vue`
- **权限**: 需要登录（`meta.requiresAuth: true`）

## 5. 组件树

```
LibraryView.vue
├── header                   # 顶部导航栏
│   ├── back-link            # 返回首页
│   ├── title                # "我的书房"
│   └── avatar-link          # 用户头像（跳转 /user）
├── main                     # 主内容区
│   ├── stats-bar            # 统计栏（总数 + 管理按钮）
│   ├── loading              # 加载状态
│   ├── book-grid            # 书架网格
│   │   └── book-card × N    # 书籍卡片
│   │       ├── checkbox     # 选中状态
│   │       ├── category-tag # 分类标签
│   │       ├── cover        # 封面
│   │       └── info         # 书名 + 大小
│   └── empty                # 空状态
├── sidebar                  # 右侧分类栏（10% 宽度）
│   ├── "全部"               # 默认选中
│   ├── category-item × N    # 分类列表
│   └── add-category         # 新建分类
├── action-bar               # 底部多选操作栏
└── category-dialog          # 分类弹窗（支持新建）
```

## 6. 数据流 & Store 设计

### Bookshelf Store

```typescript
// stores/bookshelf.ts
export const useBookshelfStore = defineStore('bookshelf', () => {
  const books = ref<BookshelfNovel[]>([]);
  const loading = ref(false);

  async function fetchBooks() { ... }       // GET /api/bookshelf
  async function removeBook(novelId) { ... } // DELETE /api/bookshelf/:id
  async function batchRemoveBooks(novelIds) { ... } // DELETE /api/bookshelf?novel_ids=...
});
```

### Category Store

```typescript
// stores/category.ts
export const useCategoryStore = defineStore('category', () => {
  const categories = ref<Category[]>([]);
  const categoryMap = computed(() => new Map(...));

  async function fetchCategories() { ... }   // GET /api/categories
  async function createCategory(name, color) { ... } // POST /api/categories
  async function deleteCategory(id) { ... }  // DELETE /api/categories/:id
  async function batchUpdateCategory(novelIds, categoryId) { ... } // PUT /api/novels/batch-category
});
```

### 数据类型

```typescript
interface BookshelfNovel {
  id: number;          // 书架记录 ID
  novel_id: number;    // 小说 ID
  title: string;
  file_size: number;
  category_id: number | null;
  added_at: string;
}

interface Category {
  id: number;
  user_id: number;
  name: string;
  color: string;
  created_at: string;
}
```

## 7. API 契约

### 书架接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/bookshelf` | GET | 获取书架列表（含小说详情） |
| `/api/bookshelf` | POST | 加入书架 |
| `/api/bookshelf/{novel_id}` | DELETE | 从书架移除 |
| `/api/bookshelf?novel_ids=1,2,3` | DELETE | 批量从书架移除 |

### 分类接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/categories` | GET | 获取分类列表 |
| `/api/categories` | POST | 创建分类 |
| `/api/categories/{id}` | PUT | 更新分类 |
| `/api/categories/{id}` | DELETE | 删除分类 |
| `/api/novels/batch-category` | PUT | 批量修改小说分类 |

### 后端模型

```python
class Bookshelf(SQLModel, table=True):
    __tablename__ = "bookshelves"
    id: int (PK)
    user_id: int (FK -> users.id)
    novel_id: int (FK -> novels.id)
    created_at: datetime

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    id: int (PK)
    user_id: int (FK -> users.id)
    name: str(50)
    color: str(20)
    created_at: datetime

# Novel 模型新增
category_id: Optional[int] (FK -> categories.id)
```

## 8. 验收标准

- [x] 顶部栏左侧显示返回按钮和标题，右侧显示用户头像
- [x] 头像点击跳转用户页面
- [x] 书架以网格形式展示书籍卡片（封面 + 书名 + 文件大小 + 分类标签）
- [x] 书架数据从 API 获取，与当前登录用户绑定
- [x] 右侧分类栏占 10% 宽度，显示「全部」和用户创建的分类
- [x] 点击分类可筛选书籍，「全部」显示所有书籍
- [x] 不同分类用不同颜色圆点区分
- [x] 侧边栏支持新建分类（内联输入框）
- [x] 长按书籍卡片可进入多选模式
- [x] 右键点击也可进入多选模式
- [x] 多选模式下点击卡片可选中/取消选中
- [x] 选中的卡片有明显视觉反馈（边框高亮 + 勾选图标）
- [x] 多选模式底部显示操作栏（已选数量 + 分类 + 删除）
- [x] 删除操作弹窗二次确认，确认文案说明后果
- [x] 分类弹窗中可选择已有分类，也可新建分类
- [x] 空书架显示空状态引导用户上传
- [x] 种子数据脚本为 test 用户创建假数据

## 9. 技术实现要点

### 前端
- [x] `useLongPress` composable 实现长按检测（支持触摸和鼠标）
- [x] BEM 命名编写样式
- [x] Element Plus 组件（el-avatar, el-button, el-dialog, el-empty, el-icon, el-input）
- [x] 删除使用 `ElMessageBox.confirm` 二次确认
- [x] Vue3 Composition API + `<script setup lang="ts">`
- [x] Bookshelf Store + API 服务
- [x] Category Store + API 服务（含预设颜色轮转）

### 后端
- [x] Bookshelf 模型（用户-小说多对多关系）
- [x] Category 模型 + CRUD API
- [x] Novel 模型新增 category_id 外键
- [x] 批量修改分类 API（修复路由冲突：放在 /{novel_id} 之前）
- [x] 删除分类时自动将关联小说设为未分类
- [x] 种子数据脚本（seed.py）

## 10. 参考 & 备注

- 参考常见阅读 App 书架布局（微信读书、起点读书）
- 封面使用纯色 + 书名前两字作为占位
- 侧边栏宽度 10%，最小 120px，最大 180px
- 批量分类路由 `/novels/batch-category` 必须在 `/novels/{novel_id}` 之前注册

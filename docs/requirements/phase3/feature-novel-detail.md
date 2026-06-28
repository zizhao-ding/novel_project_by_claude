# REQ-P3-005: 小说详情页

> **状态**: 📝 pending
> **优先级**: P1
> **创建日期**: 2026-06-28
> **最后更新**: 2026-06-28

## 1. 概述

为每本小说提供一个独立详情页，展示小说元信息（标题、简介、作者、分类、可见性标签、章节列表、统计信息等），并支持管理员在页面上直接编辑小说简介和可见性标签。详情页作为"发现 → 详情 → 阅读"链路的关键中间页，参考主流小说网站（起点、纵横等）的布局设计。

**核心能力**：
- 展示小说完整信息（标题、简介、作者、分类、可见性、章节数、总字数、上传时间）
- 章节列表，点击跳转阅读器对应章节
- "开始阅读" / "继续阅读" 快捷入口
- 管理员可在页面内直接编辑简介和可见性（无需跳转管理后台）

## 2. 用户故事

- 作为 **读者**，我想要 **在点击小说卡片后看到详情页**，以便 **了解小说内容再决定是否阅读**
- 作为 **读者**，我想要 **在详情页看到完整章节目录**，以便 **了解章节结构和跳转到指定章节**
- 作为 **读者**，我想要 **从详情页一键进入阅读**，以便 **从上次停下的地方继续阅读**
- 作为 **管理员**，我想要 **在详情页直接编辑小说简介**，以便 **完善小说信息而不必进数据库**
- 作为 **管理员**，我想要 **在详情页直接修改小说可见性标签**，以便 **快速调整内容分发策略**

## 3. UI 布局

```
┌──────────────────────────────────────────────────────────────────┐
│ ← 返回    小说详情                              🔍 搜索    👤   │  ← 顶栏（AppHeader）
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  封面图（默认占位）                                      │    │
│  │                                                         │    │
│  │  ┌──────────────────────┐                               │    │
│  │  │                      │   斗破苍穹                     │    │
│  │  │     📖 默认封面      │   作者：天蚕土豆               │    │
│  │  │                      │   [公开] [玄幻]               │    │
│  │  │                      │   共 1,623 章 · 532 万字      │    │
│  │  └──────────────────────┘   上传于 2026-06-25            │    │
│  │                                                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │  简介                                     [✏编辑] │    │    │
│  │  │  ─────────────────────────────────────────────  │    │    │
│  │  │  这里是小说简介内容，讲述了萧炎从天才到废柴，     │    │    │
│  │  │  再从废柴到大陆巅峰的逆袭故事……                   │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                                                         │    │
│  │  [开始阅读]  [加入书架]                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  📑 章节目录（共 1,623 章）                              │    │
│  │  ─────────────────────────────────────────────────────  │    │
│  │  第一章  陨落的天才                                       │    │
│  │  第二章  斗气大陆                                         │    │
│  │  第三章  客人                                             │    │
│  │  第四章  云岚宗                                           │    │
│  │  ...（分页加载，每页 50 章）                              │    │
│  │                                 (点击章节跳转阅读器)       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

管理员编辑模式：

┌──────────────────────────────────────────┐
│  ✏ 编辑小说信息                          │
│  ────────────────────────────────────── │
│                                          │
│  简介：                                  │
│  ┌────────────────────────────────────┐ │
│  │ 这里是小说简介内容……               │ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│                                          │
│  可见性标签：[公开 ▾]                    │
│  （公开 / 种子成员 / 仅管理）            │
│                                          │
│           [取消]  [保存修改]             │
└──────────────────────────────────────────┘
```

### 3.1 布局说明

| 区域 | 内容 | 说明 |
|------|------|------|
| 左侧 | 封面图 | 暂用默认占位图，后期可支持自定义封面上传 |
| 右侧上部 | 标题、作者、标签、统计 | 小说核心元信息 |
| 右侧中部 | 简介区 | 可折叠展开，管理员有编辑按钮 |
| 右侧下部 | 操作按钮 | "开始阅读"/"继续阅读" + "加入书架" |
| 下方 | 章节目录 | 分页列表，点击跳转阅读器 |

## 4. 路由 & 页面

| 路由 | 页面 | 权限 | 说明 |
|------|------|------|------|
| `/novel/:id` | `NovelDetailView.vue`（新增） | 需登录（查看详情）/ 未登录可浏览公开小说信息 | 小说详情页 |

### 4.1 入口来源

| 来源页面 | 触发方式 | 跳转路径 |
|----------|----------|----------|
| 首页（HomeView） | 点击 NovelCard | `/novel/:id` |
| 搜索页（SearchView） | 点击 NovelCard | `/novel/:id` |
| 书房页（LibraryView） | 点击书籍（普通点击，非长按） | `/novel/:id`（当前是直接进阅读器，需改为先进详情页） |
| 阅读器（ReaderView） | 顶部栏书名链接 | `/novel/:id` |

> ⚠️ **行为变更**：书房页点击书籍的默认行为从"直接进入阅读器"改为"进入详情页"，用户从详情页再进入阅读器。长按/右键多选行为不变。

### 4.2 路由守卫

```
/novel/:id
├── 未登录 → 可浏览公开小说信息，但不能阅读（"开始阅读"按钮置灰或提示登录）
├── 已登录 + 小说 public → 完整访问
├── 已登录 + 小说 seed + 角色 seed_member+ → 完整访问
└── 已登录 + 小说 admin + 角色 admin → 完整访问
    否则 → 404 或"无权访问"提示
```

## 5. 组件树

```
NovelDetailView.vue
├── AppHeader.vue                       ← 全局顶栏（返回 + 搜索 + 头像）
├── NovelDetailHeader.vue               ← 小说信息头部（封面 + 标题 + 作者 + 标签 + 统计）
│   ├── NovelCover.vue                  ← 封面图（默认占位）
│   └── NovelMetaInfo.vue               ← 元信息展示
├── NovelDescription.vue                ← 简介区（阅读模式 / 编辑模式切换）
│   └── NovelDescriptionEditor.vue      ← 简介编辑面板（仅管理员可见）
├── NovelActions.vue                    ← 操作按钮组（开始阅读 / 继续阅读 / 加入书架）
└── NovelChapterList.vue                ← 章节目录（分页列表）
    └── ChapterItem.vue                 ← 单章条目
```

## 6. 数据流 & Store 设计

### 6.1 NovelDetailStore（新增或扩展现有 NovelStore）

```typescript
// stores/novelDetail.ts
export const useNovelDetailStore = defineStore('novelDetail', () => {
  const novel = ref<NovelDetail | null>(null)   // 小说详情
  const chapters = ref<ChapterSummary[]>([])     // 章节目录
  const loading = ref(false)
  const chaptersLoading = ref(false)
  const error = ref<string | null>(null)

  // 章节分页
  const chapterPage = ref(1)
  const chapterPageSize = 50
  const chapterTotal = ref(0)

  // 编辑状态（仅管理员）
  const isEditing = ref(false)
  const editForm = ref({ description: '', visibility: 'public' })
  const saving = ref(false)

  // Actions
  async function loadNovel(id: number)          // 加载小说详情
  async function loadChapters(id: number)       // 分页加载章节列表
  async function saveEdit(id: number)           // 保存编辑（简介 + 可见性）
  function startEdit()                          // 进入编辑模式
  function cancelEdit()                         // 取消编辑

  // Getters
  const isAdmin = computed(() => ...)           // 当前用户是否管理员
  const canRead = computed(() => ...)           // 当前用户是否有阅读权限
  const hasProgress = computed(() => ...)       // 是否有阅读进度
})
```

### 6.2 类型定义扩展

```typescript
// types/novel.ts 新增

export interface NovelDetail {
  id: number;
  user_id: number;
  title: string;
  description: string;           // ← 新增：小说简介
  file_size: number;
  category_id: number | null;
  category_name?: string;        // ← 新增：分类名称
  visibility: 'public' | 'seed' | 'admin';
  username: string;              // 上传者用户名
  chapter_count: number;         // ← 新增：章节数
  word_count: number;            // ← 新增：总字数（估算）
  created_at: string;
  updated_at: string;
}

export interface ChapterSummary {
  index: number;
  title: string;
}

export interface NovelDetailPage {
  chapters: ChapterSummary[];
  total: number;
  page: number;
  page_size: number;
}
```

## 7. API 契约

### 7.1 新增 API

| 方法 | 路径 | 权限 | 说明 |
|------|------|------|------|
| GET | `/api/novels/{id}/detail` | 公开（可见性校验） | 获取小说详情 |
| PUT | `/api/novels/{id}` | admin | 修改小说信息（简介 + 可见性） |
| GET | `/api/novels/{id}/chapters` | 同详情页权限 | 分页获取章节目录 |

### 7.2 接口定义

#### 获取小说详情
```
GET /api/novels/{id}/detail
权限: 公开，但需按可见性校验（无权返回 403）
Response: {
  code: 0,
  data: {
    id: 1,
    user_id: 2,
    title: "斗破苍穹",
    description: "这里是小说简介内容...",
    file_size: 5242880,
    category_id: 1,
    category_name: "玄幻",
    visibility: "public",
    username: "tiancantudou",
    chapter_count: 1623,
    word_count: 5320000,
    created_at: "2026-06-25T10:00:00",
    updated_at: "2026-06-28T15:30:00"
  }
}
```

#### 修改小说信息（仅管理员）
```
PUT /api/novels/{id}
Body: {
  description: "更新后的小说简介...",
  visibility: "seed"
}
权限: admin
校验: 
  - description 最长 2000 字
  - visibility 必须为 public / seed / admin 之一
Response: {
  code: 0,
  message: "修改成功",
  data: { 更新后的 NovelDetail }
}
```

#### 章节目录（分页）
```
GET /api/novels/{id}/chapters?page=1&page_size=50
权限: 同小说详情可见性校验
Response: {
  code: 0,
  data: {
    chapters: [
      { index: 0, title: "第一章 陨落的天才" },
      { index: 1, title: "第二章 斗气大陆" },
      ...
    ],
    total: 1623,
    page: 1,
    page_size: 50
  }
}
```

> 注意：此接口与阅读器已有的 `GET /api/novels/{id}/chapters` 区分。阅读器接口返回带 `start_pos`/`length` 的完整数据，详情页只需 `index` + `title` 轻量数据。后端可新增参数 `?lite=true` 来区分，或新增独立端点。

### 7.3 复用 / 改造现有接口

| 接口 | 改动 |
|------|------|
| `GET /api/novels/{id}/chapters` | 新增 `?lite=true` 参数，返回轻量章节列表（仅 index + title） |
| `GET /api/novels/{id}/progress` | 详情页调用以判断"开始阅读"还是"继续阅读" |

## 8. 后端实现要点

### 8.1 Novels 模型新增字段

```python
# models/novel.py 新增
description: Optional[str] = Field(default=None, max_length=2000, description="小说简介")
```

### 8.2 数据库迁移

```sql
ALTER TABLE novels ADD COLUMN description TEXT;
```

- 使用 SQLite，直接 ALTER TABLE 即可
- 现有小说 description 默认为 NULL，详情页展示时显示"暂无简介"

### 8.3 章节统计

- `chapter_count`：从已缓存的章节数据计算（上传时已解析的章节目录）
- `word_count`：从 TXT 文件总字符数估算（中文字符 ≈ 字数），或上传时计算后存储

### 8.4 可见性校验

- 详情接口复用 `get_visible_novels_query` 逻辑
- 无权访问时返回 403（而非 404，避免信息泄露）

### 8.5 后端改动清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `app/models/novel.py` | 修改 | 新增 `description` 字段 |
| `app/schemas/novel.py` | 修改 | 新增 `NovelDetailResponse` schema |
| `app/api/novel.py` | 修改 | 新增详情接口 + 修改接口；改造章节目录接口支持 `lite` 参数 |
| `app/main.py` | 无需改动 | 路由已在 novel 模块中 |

## 9. 前端实现要点

### 9.1 入口改造

| 文件 | 改动 |
|------|------|
| `views/HomeView.vue` | NovelCard 点击跳转从直接进阅读器改为 `/novel/:id` |
| `views/SearchView.vue` | NovelCard 点击跳转改为 `/novel/:id` |
| `views/LibraryView.vue` | 普通点击改为 `/novel/:id`，长按多选行为不变 |
| `views/ReaderView.vue` | 顶部栏书名改为链接到 `/novel/:id` |

### 9.2 编辑权限控制

- 仅 `admin` 角色可见"编辑"按钮
- `usePermission` composable 提供 `isAdmin` 判断
- 编辑面板使用 Element Plus Dialog 或内联展开

### 9.3 "开始阅读" / "继续阅读" 逻辑

```
加载详情 → 查询阅读进度
  ├── 无进度 → 显示 [开始阅读] → 跳转 /reader/:id（第一章）
  └── 有进度 → 显示 [继续阅读 第X章] → 跳转 /reader/:id?chapter=X
```

### 9.4 章节目录交互

- 默认展开前 50 章，滚动加载更多
- 点击章节 → 跳转 `/reader/:id?chapter={index}`
- 当前阅读章节高亮（如果从阅读器返回）

### 9.5 响应式设计

- PC 端为主，两栏布局（封面左 + 信息右）
- 窄屏时上下堆叠

### 9.6 前端改动清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `views/NovelDetailView.vue` | **新增** | 详情页主页面 |
| `components/NovelDetailHeader.vue` | **新增** | 小说信息头部 |
| `components/NovelDescription.vue` | **新增** | 简介展示/编辑区 |
| `components/NovelChapterList.vue` | **新增** | 章节目录列表 |
| `types/novel.ts` | 修改 | 新增 `NovelDetail`、`ChapterSummary` 类型 |
| `services/novel.ts` | 修改 | 新增 `getDetail`、`updateNovel`、`getChaptersLite` 接口 |
| `stores/novelDetail.ts` | **新增** | 详情页 Store |
| `router/index.ts` | 修改 | 新增 `/novel/:id` 路由 |
| `views/HomeView.vue` | 修改 | NovelCard 点击跳转改为详情页 |
| `views/SearchView.vue` | 修改 | NovelCard 点击跳转改为详情页 |
| `views/LibraryView.vue` | 修改 | 普通点击改为跳转详情页 |
| `views/ReaderView.vue` | 修改 | 顶部栏书名链接到详情页 |

## 10. 验收标准

- [ ] 访问 `/novel/:id` 展示小说详情页，包含标题、作者、简介、分类、可见性标签、章节数、字数、上传时间
- [ ] 小说无简介时显示"暂无简介"占位文案
- [ ] 管理员可见简介旁的"编辑"按钮，点击进入编辑模式（文本域 + 可见性下拉）
- [ ] 管理员可修改简介并保存（最长 2000 字校验）
- [ ] 管理员可修改可见性标签并保存（public / seed / admin 三选一）
- [ ] 编辑保存后页面即时更新，无需刷新
- [ ] 章节目录正确展示所有章节，支持分页加载（每页 50 章）
- [ ] 点击章节跳转阅读器对应章节
- [ ] "开始阅读"按钮可点击跳转阅读器第一章
- [ ] 已有阅读进度时显示"继续阅读"，跳转到上次阅读位置
- [ ] "加入书架"按钮正常工作（复用现有书架功能）
- [ ] 无权访问的小说详情返回 403 或 404
- [ ] 首页 / 搜索页 / 书房页点击小说均跳转到详情页
- [ ] Novel 模型新增 `description` 字段，数据库正确迁移
- [ ] 后端详情接口按可见性过滤（同现有权限体系）

## 11. 依赖关系

```
REQ-P3-005 小说详情页
├── 依赖 REQ-P1-002 小说上传（Novel 模型、小说列表）
├── 依赖 REQ-P2-002 阅读器（章节列表、阅读进度）
├── 依赖 REQ-P3-004 权限系统（可见性校验、管理员判断）
├── 依赖 AppHeader（全局顶栏）
├── 依赖 NovelCard（入口来源）
├── 影响 HomeView / SearchView / LibraryView / ReaderView（入口改造）
└── 与 REQ-P3-001 国际化无直接依赖
```

## 12. 参考 & 备注

### 12.1 主流小说网站详情页参考

| 网站 | 详情页特征 |
|------|-----------|
| 起点中文网 | 封面 + 书名 + 作者 + 简介 + 标签 + 章节列表 + 打赏/月票 |
| 纵横中文网 | 封面 + 书名 + 作者 + 简介 + 字数统计 + 目录 |
| 晋江文学城 | 封面 + 书名 + 作者 + 文案 + 标签 + 章节列表 |

### 12.2 设计取舍

- **不实现封面图上传**：当前为 TXT 上传，非图片小说，后期可扩展
- **不实现评论区**：作为独立需求后续迭代
- **不实现评分/打赏**：超出当前项目范围
- **简介仅管理员可编辑**：与需求一致，上传者不可编辑（管理员统一管理内容质量）
- **可见性标签仅在详情页由管理员修改**：比当前无 UI 入口的状态（只能直接调 API）进一步

### 12.3 后续扩展可能

- 封面上传（图片小说场景）
- 评论区 / 书评
- 小说评分
- 阅读人数统计
- 标签系统（非可见性标签，而是题材标签如"热血""逆袭"）
- 作者编辑权限（允许上传者编辑自己小说的简介）

---

*本文件由 AI 在 2026-06-28 创建*

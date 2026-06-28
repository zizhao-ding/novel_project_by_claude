# REQ-P2-002: 阅读器

> **状态**: 📝 pending
> **优先级**: P1
> **创建日期**: 2026-06-28
> **最后更新**: 2026-06-28

## 1. 概述

实现小说阅读器，支持 TXT 小说的在线阅读。核心能力：智能分章、纯净阅读界面、阅读设置可调、阅读进度自动保存。前后端均需实现。

## 2. 用户故事

- 作为 **用户**，我想要 **从书架点击书籍进入阅读器**，以便 **继续阅读**
- 作为 **用户**，我想要 **看到章节目录**，以便 **快速跳转到指定章节**
- 作为 **用户**，我想要 **调整字号和主题**，以便 **舒适的阅读体验**
- 作为 **用户**，我想要 **自动保存阅读进度**，以便 **下次接着读**
- 作为 **用户**，我想要 **上一章/下一章快捷切换**，以便 **流畅阅读**

## 3. UI 布局

```
┌──────────────────────────────────────────────────────┐
│ ← 书房  斗破苍穹                    章节名  ██ %    │  ← 顶部栏（退出按钮 + 书名 + 进度）
├──────────┬───────────────────────────────┬──────────┤
│          │                               │          │
│  章节    │    正文内容区域                │          │
│  列表    │    字号可调                    │          │
│  ┌────┐  │    主题可切换                  │          │
│  │第1章│  │    支持滚轮/触控翻页          │          │
│  │第2章│  │                               │          │
│  │第3章│  │                               │          │
│  │ ... │  │                               │          │
│  └────┘  │                               │          │
│          │                               │          │
├──────────┴───────────────────────────────┴──────────┤
│  [A-] [A+]  ◎  上一章  ████████░░  下一章  [目录]  │  ← 底部工具栏
└──────────────────────────────────────────────────────┘
```

### 3.1 底部工具栏说明

| 控件 | 功能 |
|------|------|
| A- / A+ | 缩小/放大字号 |
| 主题切换 | 切换日间/夜间/护眼模式 |
| 上一章 / 下一章 | 章节导航 |
| 进度条 | 当前章节阅读进度（百分比） |
| 目录 | 打开/关闭左侧章节目录 |

## 4. 路由 & 页面

- **路由**: `/reader/:id`（`id` 为 novel_id）
- **页面**: `ReaderView.vue`
- **权限**: 需要登录（`meta.requiresAuth: true`）
- **入口**: 书房页点击书籍 → 跳转 `/reader/:id`

## 5. 组件树

```
ReaderView.vue
├── ReaderTopBar.vue          ← 顶部栏（返回 + 书名 + 章节名 + 进度）
├── ReaderSidebar.vue         ← 左侧章节列表（可折叠）
│   └── ChapterItem.vue       ← 单个章节项（高亮当前章节）
├── ReaderContent.vue         ← 正文内容区域
│   └── (纯文本渲染)           ← 根据配置渲染文字
└── ReaderToolbar.vue         ← 底部工具栏（字号、主题、导航）
    └── ReaderSettings.vue    ← 设置弹出面板（字号/主题/行间距）
```

## 6. 数据流 & Store 设计

### 6.1 ReaderStore（新增）

```typescript
// stores/reader.ts
export const useReaderStore = defineStore('reader', () => {
  const novel = ref<Novel | null>(null)       // 当前小说信息
  const chapters = ref<Chapter[]>([])          // 章节目录
  const currentChapterIndex = ref(0)           // 当前章节索引
  const currentContent = ref('')               // 当前章节正文
  const loading = ref(false)                   // 加载状态

  // 阅读设置（本地存储）
  const settings = useLocalStorage('reader-settings', {
    fontSize: 16,                              // 字号 12-24px
    theme: 'light',                            // light | dark | sepia
    lineHeight: 1.8,                           // 行间距
  })

  // 阅读进度（远程保存 + 本地缓存）
  const progress = ref<ReadingProgress | null>(null)

  // Actions
  async function loadNovel(id: number)         // 加载小说 + 章节列表
  async function loadChapter(index: number)    // 加载章节正文
  function goToNextChapter()                   // 下一章
  function goToPrevChapter()                   // 上一章
  async function saveProgress()                // 保存进度到后端
})
```

### 6.2 阅读设置（本地存储）

字号、主题、行间距为纯客户端配置，使用 `vueuse` 的 `useLocalStorage` 持久化，不涉及后端。

### 6.3 阅读进度（后端存储）

每次切换章节或滚到底部时自动保存。恢复阅读时调用接口获取最近进度。

## 7. API 契约

### 7.1 后端 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/novels/{id}/chapters` | 获取章节目录 |
| GET | `/api/novels/{id}/chapters/{index}` | 获取指定章节正文 |
| GET | `/api/novels/{id}/progress` | 获取阅读进度 |
| POST | `/api/novels/{id}/progress` | 保存阅读进度 |

### 7.2 接口定义

#### 章节目录
```
GET /api/novels/{id}/chapters
Response: {
  code: 0,
  data: {
    novel_id: number,
    chapters: [
      { index: 0, title: "第一章 陨落的天才", start_pos: 0, length: 4523 },
      { index: 1, title: "第二章 斗气大陆", start_pos: 4524, length: 3891 },
      ...
    ]
  }
}
```

#### 章节正文
```
GET /api/novels/{id}/chapters/{index}
Response: {
  code: 0,
  data: {
    index: number,
    title: string,
    content: string,          // 纯文本内容
    prev_index: number|null,  // 上一章节索引（null 表示第一章）
    next_index: number|null,   // 下一章节索引（null 表示最后一章）
  }
}
```

#### 阅读进度
```
GET /api/novels/{id}/progress
Response: {
  code: 0,
  data: {
    chapter_index: number,    // 上次阅读的章节索引
    scroll_percent: number,   // 该章节滚动百分比 (0-100)
    updated_at: string
  } | null                    // 无历史记录时返回 null
}

POST /api/novels/{id}/progress
Body: {
  chapter_index: number,
  scroll_percent: number
}
Response: { code: 0, message: "ok" }
```

## 8. 后端实现要点

### 8.1 TXT 分章逻辑

- 上传时或首次访问时，后端解析 TXT 文件
- 匹配章节标题正则：`/^第[零一二三四五六七八九十百千0-9]+[章节卷]/` 或 `/^Chapter\s+\d+/i`
- 记录每个章节的起始字节位置和长度（无需存储每章单独文件）
- 章节数据可缓存在 Novel 表新增字段 `chapter_data`（JSON 文本），或建 Chapter 表

### 8.2 阅读进度模型

```python
# models/reading_progress.py
class ReadingProgress(SQLModel, table=True):
    __tablename__ = "reading_progress"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    novel_id: int = Field(foreign_key="novels.id", index=True)
    chapter_index: int   # 当前阅读章节索引
    scroll_percent: float # 滚动百分比 0-100
    updated_at: datetime
```

每个用户对每本小说仅保留一条进度记录（upsert）。

### 8.3 文件读取优化

- 使用 `seek()` 直接定位到章节起始位置读取，避免全文加载到内存
- 章节列表首次解析后缓存在 Novel 模型字段中
- 上传小说时预先解析章节目录

## 9. 前端实现要点

### 9.1 阅读主题

| 主题 | 背景色 | 文字色 | 说明 |
|------|--------|--------|------|
| light | `#f5f5f5` | `#333` | 日间模式（默认） |
| dark | `#1a1a2e` | `#ccc` | 夜间模式 |
| sepia | `#f4ecd8` | `#4a3728` | 护眼模式 |

### 9.2 字号范围

- 最小 12px，最大 24px，默认 16px
- 步进 2px，通过 A- / A+ 按钮调节

### 9.3 阅读进度上报策略

- **保存时机**：切换章节时、关闭页面时（`beforeunload`）、手动点击保存
- **防抖**：滚动过程中每 30 秒最多上报一次（后端 upsert，无需节流过严）
- **恢复**：进入阅读器时调用 GET 接口，若返回进度则弹出提示"是否跳转到上次阅读位置"

### 9.4 章节目录侧边栏

- 左侧滑出，宽度约 250px
- 高亮当前阅读章节
- 点击章节项跳转并关闭侧边栏
- 移动端/小屏可全屏覆盖

## 10. 验收标准

- [ ] 从书房点击书籍能进入阅读器，显示第一个章节
- [ ] 左侧章节目录可正常展开/收起，点击跳转章节
- [ ] 底部工具栏可调节字号（放大/缩小）
- [ ] 可切换日间/夜间/护眼三种阅读主题
- [ ] 上一章/下一章按钮正常工作
- [ ] 阅读进度自动保存，重新进入时提示恢复
- [ ] 顶部栏显示书名和当前章节名
- [ ] 后端 TXT 分章正确解析常见中文小说格式
- [ ] 进度保存与恢复接口正常工作

---

*本文件由 AI 在 2026-06-28 创建*

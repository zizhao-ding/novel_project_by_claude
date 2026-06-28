# 阅读器模块规范

> **优先级**: P1 - 应该遵守
> **最后更新**: 2026-06-28
> **覆盖范围**: ReaderView + stores/reader.ts + services/reader.ts + 后端章节/进度 API

## 1. 模块架构

```
┌─────────────────────────────────────────────────────┐
│  ReaderView.vue                                      │
│  ┌──────────┬───────────────────────┐               │
│  │ Sidebar  │  Content Area          │               │
│  │ 章节目录  │  正文（12-24px 可调）   │               │
│  │          │  3 主题切换            │               │
│  ├──────────┴───────────────────────┤               │
│  │  Bottom Toolbar                   │               │
│  │  ←章  进度  [主题] [字号]  章→    │               │
│  └──────────────────────────────────┘               │
│                                                      │
│  stores/reader.ts                                    │
│  - chapters, currentChapter, content                 │
│  - theme, fontSize (localStorage 持久化)              │
│  - scrollPercent (保存到后端)                         │
│                                                      │
│  services/reader.ts                                  │
│  - getChapters / getChapterContent                   │
│  - getProgress / saveProgress                        │
└─────────────────────────────────────────────────────┘
```

## 2. 阅读器布局

```
┌──────────────────────────────────────────────┐
│  ← 返回  书名                         侧边栏  │  顶部
├────────┬─────────────────────────────────────┤
│        │                                     │
│ 章节   │         正文内容区                    │
│ 列表   │    （主题色背景 + 可调字号）          │
│        │                                     │
├────────┴─────────────────────────────────────┤
│  ← 上一章   30%    ☀️   A⁻  A⁺   下一章 →   │  底部
└──────────────────────────────────────────────┘
```

## 3. 三种主题

| 主题 | 背景色 | 文字色 | 说明 |
|------|--------|--------|------|
| 日间 `light` | `#ffffff` | `#333333` | 默认 |
| 夜间 `dark` | `#1a1a2e` | `#cccccc` | 暗色背景 |
| 护眼 `sepia` | `#f4ecd8` | `#5b4636` | 暖黄纸张色 |

```vue
<!-- ReaderView.vue -->
<div class="reader-page" :class="`reader-page--${theme}`">
  <!-- theme: 'light' | 'dark' | 'sepia' -->
</div>
```

```scss
.reader-page--light { background: #fff; color: #333; }
.reader-page--dark  { background: #1a1a2e; color: #ccc; }
.reader-page--sepia { background: #f4ecd8; color: #5b4636; }
```

## 4. 章节解析

### 后端 TXT 解析

```python
# app/api/novel.py
def _parse_chapters(file_path: str) -> list[dict]:
    """
    正则解析：^(第[零一二三四五六七八九十百千0-9]+[章节卷集])
    返回 [{title, start_pos, length}, ...]
    使用字节偏移量实现 O(1) 大文件读取
    """
```

### 章节导航

```
┌── 章节列表（侧边栏）──┐
│ 第1章 楔子            │
│ 第2章 初识           │  ← 点击跳转
│ 第3章 修炼           │
│ ...                   │
└──────────────────────┘

底部工具栏：
  ← 上一章  |  下一章 →
```

## 5. 阅读进度

### 数据模型

```python
# app/models/reading_progress.py
class ReadingProgress(SQLModel, table=True):
    __tablename__ = "reading_progress"
    id: int = primary_key
    user_id: int   # FK → users
    novel_id: int  # FK → novels
    chapter_index: int      # 当前章节序号
    scroll_percent: float   # 0-100
    updated_at: datetime
```

### 前后端交互

```
GET  /api/novels/{id}/progress   → 获取进度（进入阅读器时）
POST /api/novels/{id}/progress   → 保存进度（防抖，每 3 秒）
```

### 恢复提示

```
进入阅读器时：
  1. 请求 GET /progress
  2. 如果有进度记录 → 弹出提示：
     "上次读到第 X 章，滚动到 Y%。是否继续？"
     [继续阅读] [从头开始]
```

## 6. 字号调节

```typescript
// stores/reader.ts
const fontSize = ref(16); // 12-24px，默认 16px

function increaseFont() {
  if (fontSize.value < 24) fontSize.value++;
}
function decreaseFont() {
  if (fontSize.value > 12) fontSize.value--;
}
```

```vue
<!-- 模板 -->
<div class="content-area" :style="{ fontSize: fontSize + 'px' }">
  {{ content }}
</div>
```

## 7. Store 设计

```typescript
// stores/reader.ts
export const useReaderStore = defineStore('reader', () => {
  // State
  const chapters = ref<ChapterInfo[]>([]);
  const currentIndex = ref(0);
  const content = ref('');
  const loading = ref(false);

  // 本地持久化
  const settings = useLocalStorage('reader-settings', {
    theme: 'light' as const,
    fontSize: 16,
  });

  // Getters
  const currentChapter = computed(() => chapters.value[currentIndex.value]);
  const hasPrev = computed(() => currentIndex.value > 0);
  const hasNext = computed(() => currentIndex.value < chapters.value.length - 1);
  const progressPercent = computed(() => {
    if (!chapters.value.length) return 0;
    return Math.round((currentIndex.value / chapters.value.length) * 100);
  });

  // Actions
  async function loadNovel(novelId: number) { ... }
  async function goToChapter(index: number) { ... }
  function nextChapter() { if (hasNext.value) goToChapter(currentIndex.value + 1); }
  function prevChapter() { if (hasPrev.value) goToChapter(currentIndex.value - 1); }
  async function saveProgress() { ... }

  return {
    chapters, currentIndex, content, loading,
    settings,
    currentChapter, hasPrev, hasNext, progressPercent,
    loadNovel, goToChapter, nextChapter, prevChapter, saveProgress,
  };
});
```

## 8. 容器化注意事项

- ReaderView 不使用 AppHeader，全屏布局
- 监听 scroll 事件跟踪进度（`{ passive: true }` 提升性能）
- `onBeforeUnmount` 时自动保存进度 + 移除 scroll 监听
- 章节内容较大时不一次性加载（按需加载当前章节）

## 9. 验收清单

- [ ] 侧边栏显示完整章节目录，点击跳转
- [ ] 正文区支持 12-24px 字号调节
- [ ] 三种主题（日间/夜间/护眼）实时切换
- [ ] 上一章/下一章按钮 + 边界禁用
- [ ] 阅读进度自动保存（防抖 3 秒）
- [ ] 重新进入时提示恢复上次进度
- [ ] 退出时自动保存进度

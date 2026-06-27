# REQ-P1-002: 小说上传与管理

> **状态**: ✅ done
> **优先级**: P0
> **创建日期**: 2026-06-25
> **最后更新**: 2026-06-27

## 1. 概述

实现小说文件的上传、列表展示和删除功能。用户可以上传 TXT 格式的小说文件，系统自动解析并存储，用户可以查看已上传的小说列表并进行管理，支持一键加入书架。

## 2. 用户故事

- 作为 **登录用户**，我想要 **上传 TXT 小说文件**，以便 **在平台上阅读**
- 作为 **登录用户**，我想要 **查看已上传的小说列表**，以便 **管理我的藏书**
- 作为 **登录用户**，我想要 **上传后直接加入书架**，以便 **快速开始阅读**
- 作为 **登录用户**，我想要 **删除不需要的小说**，以便 **清理存储空间**

## 3. UI 布局

```
┌──────────────────────────────────────────────┐
│ ← 上传小说                         [头像]    │  ← 统一顶部栏
├──────────────────────────────────────────────┤
│ ┌────────────────────────────────────────┐   │
│ │        📁 拖拽 TXT 文件到此处           │   │
│ │        或 点击选择文件                  │   │  ← 拖拽上传区
│ │        仅支持 .txt 格式，最大 10MB      │   │
│ └────────────────────────────────────────┘   │
│                                              │
│ 已上传的小说 (6)                             │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│ │ 封面 │ │ 封面 │ │ 封面 │ │ 封面 │        │
│ │书名  │ │书名  │ │书名  │ │书名  │        │  ← 卡片网格
│ │大小  │ │大小  │ │大小  │ │大小  │        │
│ │日期  │ │日期  │ │日期  │ │日期  │        │
│ │加入  │ │加入  │ │加入  │ │加入  │        │
│ │ 删除 │ │ 删除 │ │ 删除 │ │ 删除 │        │
│ └──────┘ └──────┘ └──────┘ └──────┘        │
└──────────────────────────────────────────────┘
```

## 4. 路由 & 页面

| 路由路径 | 页面名称 | 视图文件 | 认证要求 |
|----------|----------|----------|----------|
| `/upload` | `Upload` | `UploadView.vue` | 是 |

## 5. 组件树

```
UploadView.vue
├── header                   # 统一顶部导航栏
│   ├── back-link            # 返回书房
│   ├── title                # "上传小说"
│   └── avatar-link          # 用户头像（跳转 /user）
├── upload-card              # 上传区域卡片
│   ├── ElUpload (drag)      # 拖拽上传组件
│   └── progress             # 上传进度条
├── section-header           # 列表标题（已上传的小说 + 数量）
├── novel-grid               # 小说卡片网格
│   └── novel-card × N       # 小说卡片
│       ├── cover            # 封面（纯色 + 书名前两字）
│       ├── info             # 书名 + 大小 + 日期
│       └── actions          # 加入书架 + 删除
└── empty                    # 空状态提示
```

## 6. 数据流 & Store 设计

### Store: `useNovelStore`

```typescript
State:
  novels: Novel[]                 # 小说列表
  uploading: boolean              # 是否正在上传
  uploadProgress: number          # 上传进度 (0-100)
  loading: boolean                # 是否正在加载列表
  error: string | null            # 错误信息

Actions:
  uploadNovel(file)               # 上传小说文件
  fetchNovels()                   # 获取小说列表
  deleteNovel(id)                 # 删除小说（纯操作，确认由调用方处理）
```

### 数据结构

```typescript
interface Novel {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  category_id: number | null;
  created_at: string;
}
```

## 7. API 契约

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/upload/novel` | 上传小说 | FormData: `file` | `{ code, message, data: Novel }` |
| GET | `/api/novels` | 获取小说列表 | Query: `page`, `page_size` | `{ code, message, data: { items: Novel[], total } }` |
| DELETE | `/api/novels/{id}` | 删除小说 | - | `{ code, message }` |
| POST | `/api/bookshelf` | 加入书架 | `{ novel_id }` | `{ code, message }` |

## 8. 验收标准

### 场景 1: 上传 TXT 小说成功

- [x] 用户在上传页拖拽或选择 TXT 文件
- [x] 系统校验文件格式（仅支持 .txt）
- [x] 系统校验文件大小（最大 10MB）
- [x] 显示上传进度（图标 + 百分比 + 进度条）
- [x] 上传成功后显示"上传成功"提示
- [x] 新小说出现在已上传列表中

### 场景 2: 上传格式校验

- [x] 用户尝试上传非 TXT 文件
- [x] 显示"仅支持 TXT 格式"错误提示
- [x] 不发起上传请求

### 场景 3: 上传大小校验

- [x] 用户尝试上传超过 10MB 的文件
- [x] 显示"文件大小不能超过 10MB"错误提示
- [x] 不发起上传请求

### 场景 4: 查看小说列表

- [x] 用户进入上传页
- [x] 自动加载当前用户的小说列表
- [x] 以卡片网格形式展示（封面 + 书名 + 大小 + 日期）
- [x] 列表为空时显示空状态引导

### 场景 5: 加入书架

- [x] 用户点击卡片的"加入书架"按钮
- [x] 调用加入书架 API
- [x] 成功后显示"已加入书架"提示

### 场景 6: 删除小说

- [x] 用户点击卡片的"删除"按钮
- [x] 弹出确认对话框（含小说名称）
- [x] 用户确认后调用删除 API
- [x] 删除成功后从小说列表中移除
- [x] 用户取消则不执行删除

### 场景 7: 页面导航

- [x] 顶部栏左侧显示返回按钮（跳转书房）和标题
- [x] 顶部栏右侧显示用户头像（跳转用户页）

## 9. 技术实现要点

- [x] Element Plus ElUpload 组件（drag 模式）
- [x] 文件格式校验：accept=".txt" + 后端二次校验
- [x] 文件大小校验：前端 10MB 限制 + 后端二次校验
- [x] 上传进度：通过 Axios onUploadProgress 回调
- [x] 删除二次确认：使用 ElMessageBox.confirm（含小说名称）
- [x] 加入书架：调用 bookshelfApi.add
- [x] 卡片布局：与书房页风格统一
- [x] 统一顶部栏：与书房页、用户页风格一致
- [x] Store 职责分离：deleteNovel 只做删除，确认弹窗在视图层

## 10. 参考 & 备注

- **核心规范**: `docs/specs/core/coding-standards.md`
- **架构规范**: `docs/specs/core/architecture.md`
- **前端实现**: `frontend_project/src/views/UploadView.vue`
- **Store 实现**: `frontend_project/src/stores/novel.ts`
- **API 实现**: `frontend_project/src/services/novel.ts`
- **后端实现**: `backend_project/app/api/novel.py`

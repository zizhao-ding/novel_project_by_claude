# REQ-P1-002: 小说上传与管理

> **状态**: ✅ 已完成
> **优先级**: P0 核心
> **创建日期**: 2026-06-25
> **最后更新**: 2026-06-25

## 1. 概述

实现小说文件的上传、列表展示和删除功能。用户可以上传 TXT 格式的小说文件，系统自动解析并存储，用户可以查看已上传的小说列表并进行管理。

## 2. 用户故事

- 作为 **登录用户**，我想要 **上传 TXT 小说文件**，以便 **在平台上阅读**
- 作为 **登录用户**，我想要 **查看已上传的小说列表**，以便 **管理我的藏书**
- 作为 **登录用户**，我想要 **删除不需要的小说**，以便 **清理存储空间**

## 3. UI 布局

### 上传页
```
┌──────────────────────────────────────────┐
│                                          │
│         📚 上传小说                       │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │                                    │  │
│  │     📁 拖拽 TXT 文件到此处          │  │
│  │     或 点击选择文件                 │  │
│  │                                    │  │
│  │     仅支持 .txt 格式，最大 10MB     │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  已上传的小说                       │  │
│  │                                    │  │
│  │  | 书名     | 大小   | 上传时间 | 操作 |  │
│  │  |----------|--------|----------|------|  │
│  │  | 小说A    | 1.2 MB | 2026-06  | 删除 |  │
│  │  | 小说B    | 856 KB | 2026-06  | 删除 |  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## 4. 路由 & 页面

| 路由路径 | 页面名称 | 视图文件 | 认证要求 |
|----------|----------|----------|----------|
| `/upload` | `Upload` | `UploadView.vue` | 是 |

## 5. 组件树

```
UploadView.vue
├── ElCard                         # 上传区域卡片
│   ├── ElUpload (drag)            # 拖拽上传组件
│   │   └── UploadFilled (icon)    # 上传图标
│   └── ElProgress                 # 上传进度条
├── ElCard                         # 已上传列表卡片
│   └── ElTable                    # 小说列表表格
│       ├── ElTableColumn (书名)
│       ├── ElTableColumn (大小)
│       ├── ElTableColumn (上传时间)
│       └── ElTableColumn (操作 - 删除按钮)
└── ElEmpty                        # 空状态提示
```

## 6. 数据流 & Store 设计

### Store: `useNovelStore`

```
State:
  novels: Novel[]                 # 小说列表
  uploading: boolean              # 是否正在上传
  uploadProgress: number          # 上传进度 (0-100)
  loading: boolean                # 是否正在加载列表
  error: string | null            # 错误信息

Actions:
  uploadNovel(file)               # 上传小说文件
  fetchNovels()                   # 获取小说列表
  deleteNovel(id)                 # 删除小说（含二次确认）
```

### 数据结构

```typescript
interface Novel {
  id: number;
  user_id: number;
  title: string;
  file_size: number;
  created_at: string;
}
```

## 7. API 契约

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/upload/novel` | 上传小说 | FormData: `file` | `{ code, message, data: Novel }` |
| GET | `/api/novels` | 获取小说列表 | Query: `page`, `page_size` | `{ code, message, data: { items: Novel[], total } }` |
| DELETE | `/api/novels/{id}` | 删除小说 | - | `{ code, message }` |

## 8. 验收标准

### 场景 1: 上传 TXT 小说成功

- [x] 用户在上传页拖拽或选择 TXT 文件
- [x] 系统校验文件格式（仅支持 .txt）
- [x] 系统校验文件大小（最大 10MB）
- [x] 显示上传进度条
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
- [x] 显示书名、文件大小、上传时间
- [x] 列表为空时显示"暂未上传小说"

### 场景 5: 删除小说

- [x] 用户点击小说的"删除"按钮
- [x] 弹出确认对话框"删除后不可恢复，确定要删除吗？"
- [x] 用户确认后调用删除 API
- [x] 删除成功后从小说列表中移除
- [x] 显示"删除成功"提示
- [x] 用户取消则不执行删除

### 场景 6: 未登录访问上传页

- [x] 用户未登录时尝试访问 /upload
- [x] 自动跳转到 /login?redirect=/upload
- [x] 登录后自动跳转回 /upload

## 9. 技术实现要点

- [x] 使用 Element Plus ElUpload 组件（drag 模式）
- [x] 文件格式校验：accept=".txt" + 后端二次校验
- [x] 文件大小校验：前端 10MB 限制 + 后端二次校验
- [x] 上传进度：通过 Axios onUploadProgress 回调
- [x] 删除二次确认：使用 ElMessageBox.confirm
- [x] 文件存储：本地文件系统 `uploads/novels/`
- [x] 文件命名：`{user_id}_{timestamp}_{filename}`
- [x] 后端权限校验：只能删除自己的小说
- [x] 后端同时删除文件和数据库记录

## 10. 参考 & 备注

- **核心规范**: `docs/specs/core/coding-standards.md`
- **架构规范**: `docs/specs/core/architecture.md`
- **Hook 规则**: `docs/specs/core/hook-rules.md`
- **前端实现**: `front_project/src/views/UploadView.vue`
- **Store 实现**: `front_project/src/stores/novel.ts`
- **API 实现**: `front_project/src/services/novel.ts`
- **后端实现**: `backend_project/app/api/novel.py`
- **数据模型**: `backend_project/app/models/novel.py`
- **Schema**: `backend_project/app/schemas/novel.py`

# 小说上传功能

> **状态**: ✅ 已完成
> **优先级**: P0 核心
> **关联 Spec**: 01_auth_register（依赖登录状态）

## 1. 概述

用户登录后可上传 TXT 小说文件，系统存储至本地文件系统，数据库记录元信息。支持查看上传列表和删除。

## 2. 用户故事

- 作为 **登录用户**，我想要 **上传本地 TXT 小说文件**，以便 **在线阅读我的个人藏书**
- 作为 **用户**，我想要 **看到上传进度**，以便 **了解上传状态**
- 作为 **用户**，我想要 **查看已上传的小说列表**，以便 **管理我的藏书**

## 3. UI 布局

```
┌──────────────────────────────────────────┐
│  导航栏（已登录状态）                      │
├──────────────────────────────────────────┤
│  ┌────────────────────────────────────┐  │
│  │        📤 点击或拖拽上传            │  │
│  │       支持 TXT 格式，最大 10MB      │  │
│  │       [    选择文件    ]            │  │
│  └────────────────────────────────────┘  │
│                                          │
│  已上传的小说：                           │
│  ┌────────────────────────────────────┐  │
│  │  凡人修仙传.txt  2.4MB  2026-06-21 │  │
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
├── ElUpload（拖拽 + 选择文件）
│   └── beforeUpload 校验（格式、大小）
├── ElProgress（上传进度，v-if 上传中）
└── 已上传列表
    └── ElTable / ElCard（v-for，含删除按钮）
```

## 6. 数据流 & Store 设计

### Store: `useNovelStore`

```
State:
  novels: Novel[]           # 已上传列表
  uploading: boolean        # 是否有上传中
  uploadProgress: number    # 0-100
  loading: boolean
  error: string | null

Actions:
  uploadNovel(file: File)   # 上传 → 更新 progress → 加入列表
  fetchNovels()             # 获取列表
  deleteNovel(id)           # 删除
```

## 7. API 契约

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/upload/novel` | 上传 | FormData (file) | `ApiResponse<Novel>` |
| GET | `/api/novels` | 列表 | Query: page, pageSize | `{ code, data: { items, total } }` |
| DELETE | `/api/novels/:id` | 删除 | - | `ApiResponse` |

## 8. 验收标准

### 场景 1: 上传成功
```
Given 用户已登录且在 /upload 页面
When  用户选择 TXT 文件并上传
Then  显示上传进度条
     完成后提示"上传成功"
     小说出现在列表中
```

### 场景 2: 格式校验
```
Given 用户已登录
When  用户选择非 TXT 文件
Then  上传前拦截，提示"仅支持 TXT 格式"
```

### 场景 3: 大小校验
```
Given 用户已登录
When  用户选择超过 10MB 的文件
Then  上传前拦截，提示"文件大小不能超过 10MB"
```

### 场景 4: 未登录拦截
```
Given 用户未登录
When  用户访问 /upload
Then  跳转到 /login?redirect=/upload
```

## 9. 技术实现要点

- [x] 前端：UploadView.vue（拖拽上传 + 进度 + 列表 + 删除）
- [x] 前端：useNovelStore（上传 + 列表管理）
- [x] 前端：services/novel.ts（novel API 封装）
- [x] 前端：types/novel.ts（Novel 类型定义）
- [x] 后端：Novel 模型 + 建表
- [x] 后端：POST /api/upload/novel（接收文件 → 存盘 → 写DB）
- [x] 后端：GET /api/novels（按用户查小说列表）
- [x] 后端：DELETE /api/novels/:id（删文件 + 删DB）
- [x] 创建 `backend_project/uploads/novels/` 目录
- [x] 新增依赖 python-multipart

## 10. 存储方案

采用 **本地文件系统**（方案1）。

```
backend_project/uploads/novels/
├── 1_1766668800_斗破苍穹.txt     # {user_id}_{timestamp}_{原文件名}
├── 1_1766668900_凡人修仙传.txt
└── ...
```

数据库只存文件路径和元信息，不存文件内容。

## 参考 & 备注

- 相关 Rules: 02_vue3, 04_store, 05_api, 07_routing, 08_error
- 后端已有认证体系，上传需 Bearer Token

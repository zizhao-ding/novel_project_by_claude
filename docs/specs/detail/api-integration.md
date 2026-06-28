# API 集成详细指南

> **优先级**: P1 - 应该遵守
> **最后更新**: 2026-06-28
> **基于**: services/api.ts, auth.ts, novel.ts 等实际 API 服务模式

## 1. 架构总览

```
组件/Store
    ↓
services/xxxApi.ts      # 业务 API 函数
    ↓
services/api.ts         # ApiService 类（Axios 封装）
    ↓
后端 FastAPI             # /api/* 路由
```

## 2. Axios 实例封装

`services/api.ts` 是唯一的 HTTP 客户端实例：

```typescript
class ApiService {
  private instance: AxiosInstance;

  constructor() {
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' },
    });
    this.setupInterceptors();
  }

  // 请求拦截：自动附加 Token
  // 响应拦截：统一处理 401/500 + 解包 response.data
}
```

### 关键行为

- 响应拦截器 `return response.data` —— 调用方拿到的就是 `response.data`
- 401 自动清除 token 并提示"登录已过期"
- 500+ 统一提示"服务器错误"

## 3. 业务 API 定义

### 标准模式

```typescript
// services/example.ts
import { api } from './api';

export const exampleApi = {
  getList: (params: { page?: number; pageSize?: number }) =>
    api.client.get<{ code: number; data: { items: any[]; total: number } }>(
      '/examples',
      { params }
    ),

  getById: (id: number) =>
    api.client.get<{ code: number; data: any }>(`/examples/${id}`),

  create: (data: FormData) =>
    api.client.post<{ code: number; data: any }>('/examples', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  update: (id: number, data: Record<string, any>) =>
    api.client.put<{ code: number; data: any }>(`/examples/${id}`, data),

  delete: (id: number) =>
    api.client.delete<{ code: number }>(`/examples/${id}`),
};
```

### 命名规范

| HTTP 方法 | 函数名 | 示例 |
|-----------|--------|------|
| GET 列表 | `getList` | `novelApi.getList(params)` |
| GET 单个 | `getById` | `novelApi.getById(id)` |
| POST 创建 | `create` / `upload` | `authApi.register(data)` |
| PUT 更新 | `update` | `novelApi.updateVisibility(id, vis)` |
| DELETE 删除 | `delete` | `novelApi.delete(id)` |

## 4. 后端 API 响应规范

### 标准格式

```typescript
// 所有后端接口返回统一格式
interface ApiResponse<T> {
  code: number;    // 0 = 成功，非 0 = 错误
  message: string; // 提示信息
  data?: T;        // 业务数据
}
```

### 分页格式

```typescript
// 请求
{ page: number; page_size: number }

// 响应
{
  code: 0,
  message: "成功",
  data: {
    items: T[],
    total: number
  }
}
```

## 5. 前端服务文件清单

| 文件 | 职责 | API 前缀 |
|------|------|----------|
| `api.ts` | Axios 实例 + 拦截器 | — |
| `auth.ts` | 注册/登录/资料/统计/改密 | `/api/auth` |
| `novel.ts` | 小说 CRUD + 可见性 | `/api` |
| `reader.ts` | 章节列表/内容/阅读进度 | `/api/novels/{id}` |
| `bookshelf.ts` | 书架增删查 | `/api/bookshelf` |
| `category.ts` | 分类 CRUD | `/api/categories` |
| `home.ts` | 热门/最新 | `/api/novels` |
| `search.ts` | 搜索 | `/api/novels/search` |
| `admin.ts` | 用户管理/角色修改 | `/api/admin` |

## 6. 错误处理层级

```
┌──────────────────────────────────────────┐
│ 1. ApiService 拦截器                      │
│    401 → 清除登录 / 500+ → 服务器错误     │
├──────────────────────────────────────────┤
│ 2. Store Action                          │
│    try-catch → ElMessage.error + 设置 error state │
├──────────────────────────────────────────┤
│ 3. View 组件                             │
│    根据 store.error / store.loading 展示 UI │
└──────────────────────────────────────────┘
```

### 新增业务 API 的步骤

1. 在 `services/` 下新建文件
2. 导出 `xxxApi` 常量对象
3. 所有方法通过 `api.client` 调用
4. 泛型标注返回类型
5. 需要 multipart 时设置 `Content-Type: multipart/form-data`

## 7. 类型定义规范

### 原则：类型放 types/，不在 services/ 中重复定义

```typescript
// ✅ types/novel.ts
export interface Novel {
  id: number;
  title: string;
  // ...
}

// ✅ services/novel.ts
import type { Novel } from '@/types/novel';

// ❌ services/reader.ts 中重复定义 ChapterInfo（stores/reader.ts 也有）
```

### 当前已知的类型重复（待清理）

| 类型 | 重复位置 |
|------|----------|
| `ChapterInfo` | `stores/reader.ts` + `services/reader.ts` |
| `ReadingProgress` | `stores/reader.ts` + `services/reader.ts` |
| `HotNovelItem` | `stores/home.ts` + `services/home.ts` |
| `NovelItem` | `stores/home.ts` + `services/home.ts` |

## 8. 关键约束速查

- ✅ 所有 HTTP 请求必须通过 `api.client` 发起
- ✅ 业务 API 按领域分文件，导出为 `xxxApi` 常量
- ✅ 请求/响应必须泛型标注类型
- ✅ 类型定义集中在 `types/`，禁止在 services/ 中重复定义
- ❌ 禁止在组件中直接使用 axios 或 fetch
- ❌ 禁止硬编码 API URL
- ❌ 禁止在 services/ 中定义业务类型（应放在 types/）

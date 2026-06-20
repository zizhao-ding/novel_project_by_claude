# 05 — API 服务层规范

## 架构

```
services/
├── api.ts              # Axios 实例封装（基地址、拦截器）
├── auth.ts             # 认证相关 API
├── novel.ts            # 小说相关 API
├── image.ts            # 图片相关 API
└── bookmark.ts         # 书签相关 API
```

## Axios 实例封装

```typescript
// services/api.ts
import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';

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

  private setupInterceptors() {
    // 请求拦截：自动附加 Token
    this.instance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
      const userStore = useUserStore();
      if (userStore.token) {
        config.headers.Authorization = `Bearer ${userStore.token}`;
      }
      return config;
    });

    // 响应拦截：统一错误处理
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => response.data,
      (error) => {
        if (error.response?.status === 401) {
          useUserStore().logout();
          ElMessage.error('登录已过期，请重新登录');
        } else if (error.response?.status >= 500) {
          ElMessage.error('服务器错误，请稍后重试');
        }
        return Promise.reject(error);
      }
    );
  }

  get client() { return this.instance; }
}

export const api = new ApiService();
```

## 业务 API 定义

```typescript
// services/novel.ts
import { api } from './api';
import type { Novel, NovelListParams, PaginatedResponse } from '@/types/novel';

export const novelApi = {
  getList: (params: NovelListParams) =>
    api.client.get<PaginatedResponse<Novel>>('/novels', { params }),

  getById: (id: number) =>
    api.client.get<Novel>(`/novels/${id}`),

  getContent: (id: number) =>
    api.client.get<string>(`/novels/${id}/content`),

  upload: (data: FormData) =>
    api.client.post<Novel>('/novels', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  update: (id: number, data: Partial<Novel>) =>
    api.client.put<Novel>(`/novels/${id}`, data),

  delete: (id: number) =>
    api.client.delete(`/novels/${id}`),
};
```

## 规范要点

- ✅ API 函数按业务领域分文件
- ✅ 使用对象字面量组织 API 方法，导出为常量
- ✅ 统一通过 `api.client` 实例发送请求
- ✅ 接口响应需要泛型标注返回类型
- ❌ 禁止在组件中直接使用 `axios` 或 `fetch`
- ❌ 禁止硬编码 API URL

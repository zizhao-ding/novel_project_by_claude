# 03 — TypeScript 类型规范

## 核心约束

**所有新代码必须使用 TypeScript。** `.vue` 文件使用 `<script setup lang="ts">`，工具文件使用 `.ts` 扩展名。

## 命名规范

```typescript
// ✅ 接口：PascalCase
export interface User {
  id: number;
  username: string;
  email: string;
  createdAt: Date;
}

// ✅ 类型别名：PascalCase
export type UserRole = 'admin' | 'editor' | 'viewer';

// ✅ 枚举：PascalCase
export enum HttpStatus {
  SUCCESS = 200,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  NOT_FOUND = 404,
  SERVER_ERROR = 500,
}
```

## 泛型规范

```typescript
// ✅ 简单泛型使用 T, K, V 等单字母
export function useState<T>(initial: T): [Ref<T>, (v: T) => void] {
  // ...
}

// ✅ 复杂泛型使用描述性名称
export interface ApiResponse<TData, TError = Error> {
  data?: TData;
  error?: TError;
  loading: boolean;
}

// ✅ API 响应泛型封装
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}
```

## 类型文件组织

```typescript
// types/novel.ts — 按业务领域划分类型文件
export interface Novel {
  id: number;
  userId: number;
  title: string;
  description: string;
  filePath: string;
  fileSize: number;
  pageCount: number;
  views: number;
  createdAt: string;
}

export interface NovelListParams {
  page: number;
  pageSize: number;
  search?: string;
}

export type NovelStatus = 'draft' | 'published' | 'archived';
```

## ✅ 正确 vs ❌ 错误

```typescript
// ✅ 使用 interface 定义对象形状
interface Novel { id: number; title: string; }

// ✅ 使用 type 定义联合/交叉类型
type Status = 'active' | 'inactive';

// ❌ 避免使用 any
// const data: any = response;

// ✅ 使用 unknown 并在使用时做类型守卫
const data: unknown = response;
if (isNovel(data)) { /* data 此时是 Novel 类型 */ }

// ❌ 禁止使用 @ts-ignore
// ✅ 使用 @ts-expect-error 留下记录
```

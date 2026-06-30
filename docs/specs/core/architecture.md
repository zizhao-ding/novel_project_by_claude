# 架构规范 (Architecture)

> **所属层级**: AI Agent 六层架构 — **规范层**（建议性标准）
> **优先级**: P0 - 必须遵守
> **最后更新**: 2026-06-30
>
> ⚠️ **架构演进说明**：项目已从 Harness 六层架构（需求→规范→方案→执行→审核→验收）迁移到 **AI Agent 原生六层架构**（规范层·上下文层·约束层·记忆层·工具层·工作流层）。本文档内容归属新架构的**规范层**——定义代码质量、架构模式的标准做法。
>
> 架构总纲：`docs/specs/core/ai-agent-architecture.md`
> 硬性约束：`docs/specs/core/constraint-layer.md`

## 1. 状态管理规范 (Pinia)

### 核心原则

1. **使用 Setup Store 模式**（`defineStore('name', () => { ... })`），禁止 Options Store
2. **Store 文件放在 `src/stores/`**，一个 store 一个文件
3. **组件中使用 `storeToRefs` 解构**以保持响应性

### Store 标准模板

```typescript
// stores/novel.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Novel } from '@/types/novel';
import { novelApi } from '@/services/novel';

export const useNovelStore = defineStore('novel', () => {
  // ── State ──
  const novels = ref<Novel[]>([]);
  const currentNovel = ref<Novel | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // ── Getters (Computed) ──
  const novelCount = computed(() => novels.value.length);
  const publishedNovels = computed(() =>
    novels.value.filter(n => n.status === 'published')
  );

  // ── Actions ──
  async function fetchNovels() {
    loading.value = true;
    error.value = null;
    try {
      novels.value = await novelApi.getList();
    } catch (err) {
      error.value = (err as Error).message;
    } finally {
      loading.value = false;
    }
  }

  async function addNovel(data: FormData) {
    const novel = await novelApi.upload(data);
    novels.value.unshift(novel);
    return novel;
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    novels, currentNovel, loading, error,
    // Getters
    novelCount, publishedNovels,
    // Actions
    fetchNovels, addNovel, clearError,
  };
});
```

### Store 使用规范

```vue
<script setup lang="ts">
import { useNovelStore } from '@/stores/novel';
import { storeToRefs } from 'pinia';

const novelStore = useNovelStore();
// ✅ 使用 storeToRefs 解构 state/getters，保持响应性
const { novels, loading, error, novelCount } = storeToRefs(novelStore);
// ✅ Actions 直接从 store 实例解构
const { fetchNovels, addNovel } = novelStore;

onMounted(() => {
  fetchNovels();
});
</script>
```

### 命名约定

| 类别 | 命名方式 | 示例 |
|------|----------|------|
| Store 文件名 | 名词单数 | `user.ts`, `novel.ts` |
| Store 实例 | `use` + 名词 + `Store` | `useUserStore`, `useNovelStore` |
| State | 名词 | `novels`, `loading`, `error` |
| Getter | 名词/形容词 | `novelCount`, `isAuthenticated` |
| Action | 动词 | `fetchNovels`, `addNovel`, `removeNovel` |

### ❌ 禁止事项

- ❌ 禁止使用 Options Store（`state: () => ({...})`）
- ❌ 禁止直接修改 state（必须通过 action）
- ❌ 禁止解构 state 时不用 `storeToRefs`（会丢失响应性）

## 2. API 服务层规范

### 架构

```
services/
├── api.ts              # Axios 实例封装（基地址、拦截器）
├── auth.ts             # 认证相关 API
├── novel.ts            # 小说相关 API
├── image.ts            # 图片相关 API
└── bookmark.ts         # 书签相关 API
```

### Axios 实例封装

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

### 业务 API 定义

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

### 规范要点

- ✅ API 函数按业务领域分文件
- ✅ 使用对象字面量组织 API 方法，导出为常量
- ✅ 统一通过 `api.client` 实例发送请求
- ✅ 接口响应需要泛型标注返回类型
- ❌ 禁止在组件中直接使用 `axios` 或 `fetch`
- ❌ 禁止硬编码 API URL

## 3. 路由规范

### 路由配置标准

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),  // ✅ 懒加载
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('@/views/LibraryView.vue'),
    meta: { requiresAuth: true, title: '我的书房' },
  },
  {
    path: '/reader/:id',
    name: 'Reader',
    component: () => import('@/views/ReaderView.vue'),
    props: true,  // 将路由参数作为 props 传入组件
    meta: { title: '阅读' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
```

### 路由守卫

```typescript
// router/guards.ts
import type { Router } from 'vue-router';
import { useUserStore } from '@/stores/user';

export function setupRouterGuards(router: Router) {
  router.beforeEach((to, from, next) => {
    const userStore = useUserStore();
    const requiresAuth = to.matched.some(r => r.meta.requiresAuth);

    if (requiresAuth && !userStore.isAuthenticated) {
      next({ name: 'Login', query: { redirect: to.fullPath } });
    } else {
      next();
    }
  });

  // 全局后置守卫：设置页面标题
  router.afterEach((to) => {
    const title = to.meta.title as string;
    document.title = title ? `${title} | 小说阅读平台` : '小说阅读平台';
  });
}
```

### Meta 字段约定

```typescript
// 路由 meta 字段使用声明
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;   // 是否需要登录
    title?: string;           // 页面标题
    hideNavbar?: boolean;     // 是否隐藏导航栏
    roles?: string[];         // 允许访问的角色
  }
}
```

### 命名规范

| 项目 | 命名方式 | 示例 |
|------|----------|------|
| 路由 `name` | PascalCase | `Home`, `NovelDetail` |
| 路由 `path` | kebab-case | `/novel-list`, `/reader/:id` |
| 视图文件 | `*View.vue` | `HomeView.vue`, `LibraryView.vue` |

### ✅ 规则速查

- ✅ 所有页面组件**必须懒加载**（`() => import(...)`）
- ✅ 需要认证的路由设置 `meta.requiresAuth = true`
- ✅ 传递路由参数优先使用 `props: true`
- ✅ 登录后重定向回原页面（通过 `redirect` query 参数）
- ❌ 禁止直接导入视图组件（破坏代码分割）

## 4. 错误处理规范

### 全局错误处理

```typescript
// plugins/error-handler.ts
import type { App } from 'vue';
import { ElMessage } from 'element-plus';

export function setupErrorHandler(app: App) {
  // Vue 全局错误捕获
  app.config.errorHandler = (err, instance, info) => {
    console.error('[Global Error]', err);
    console.error('[Error Info]', info);
    ElMessage.error('系统出现错误，请稍后重试');
  };

  // 未处理的 Promise 拒绝
  window.addEventListener('unhandledrejection', (event) => {
    console.error('[Unhandled Promise]', event.reason);
    ElMessage.error('网络请求失败，请检查网络连接');
    event.preventDefault();
  });
}
```

### 异步操作错误处理

```typescript
// ✅ 标准模式：try-catch-finally
async function fetchData() {
  loading.value = true;
  error.value = null;
  try {
    const data = await api.getData();
    return data;
  } catch (err) {
    error.value = (err as Error).message;
    ElMessage.error(`加载失败：${error.value}`);
    throw err;
  } finally {
    loading.value = false;
  }
}
```

### Store Action 错误处理

```typescript
// ✅ Store action 捕获错误并设置 error state
async function uploadNovel(data: FormData) {
  loading.value = true;
  error.value = null;
  try {
    const novel = await novelApi.upload(data);
    novels.value.unshift(novel);
    ElMessage.success('上传成功');
    return novel;
  } catch (err) {
    const msg = (err as Error).message;
    error.value = msg;
    ElMessage.error(`上传失败：${msg}`);
    throw err;
  } finally {
    loading.value = false;
  }
}
```

### HTTP 错误码处理

| 状态码 | 处理方式 |
|--------|----------|
| 400 | 显示后端返回的错误消息 |
| 401 | 清除登录状态，跳转登录页 |
| 403 | 提示"无权限访问" |
| 404 | 提示"资源不存在" |
| 500+ | 提示"服务器错误，请稍后重试" |
| Network Error | 提示"网络连接失败，请检查网络" |

### ✅ 规则速查

- ✅ 所有 `async` 操作必须有 `try-catch`
- ✅ 捕获错误后必须给用户可见的提示（ElMessage）
- ✅ API 层错误由拦截器统一处理，业务层处理业务错误
- ❌ 禁止吞掉错误不处理（空 `catch` 块）
- ❌ 禁止将原始错误对象直接展示给用户

## 5. 敏感操作二次确认规范

### 核心原则

任何**不可逆或高风险操作**，执行前必须弹出确认对话框，用户确认后才执行。

### 需要二次确认的操作

| 类别 | 操作 |
|------|------|
| 删除 | 删除小说、删除书签、删除账号、删除文件 |
| 退出 | 退出登录 |
| 覆盖 | 覆盖已有文件、替换内容 |
| 发布 | 公开发布内容 |

### 实现方式

统一使用 `ElMessageBox.confirm`：

```typescript
import { ElMessageBox, ElMessage } from 'element-plus';

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm(
      '删除后不可恢复，确定要删除吗？',
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    // 用户确认后执行
    await api.deleteItem(id);
    ElMessage.success('删除成功');
  } catch {
    // 用户取消，不做任何操作
  }
}
```

### 标准模板

```typescript
// ✅ 正确：先确认再执行
async function handleSensitiveAction() {
  try {
    await ElMessageBox.confirm('提示文案', '确认标题', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    // 执行操作...
  } catch {
    // 用户取消
  }
}

// ❌ 错误：直接执行
async function handleDelete(id: number) {
  await api.delete(id); // 没有确认步骤！
}
```

### ❌ 禁止事项

- ❌ 删除操作禁止不弹窗确认直接执行
- ❌ 退出登录禁止不弹窗确认

### ✅ 规则速查

- ✅ 所有删除操作必须用 `ElMessageBox.confirm` 二次确认
- ✅ 退出、覆盖等敏感操作同理
- ✅ 确认文案要明确说明后果（如「不可恢复」）

## 6. 版本管理规范

### 核心原则

使用**阶段前缀**区分不同开发阶段的需求，便于版本规划和进度追踪。

### 阶段命名规则

| 阶段 | 前缀 | 说明 | 示例 |
|------|------|------|------|
| Phase 1 | `P1` | 核心功能阶段 | REQ-P1-001, REQ-P1-002 |
| Phase 2 | `P2` | 功能扩展阶段 | REQ-P2-001, REQ-P2-002 |
| Phase 3 | `P3` | 功能完善阶段 | REQ-P3-001, REQ-P3-002 |

### 需求编号格式

```
REQ-{阶段}-{序号}

示例：
REQ-P1-001  # Phase 1 第 1 个需求
REQ-P1-002  # Phase 1 第 2 个需求
REQ-P2-001  # Phase 2 第 1 个需求
```

### 目录结构

```
docs/requirements/
├── index.md                    # 需求索引（包含所有阶段）
├── _template.md                # 需求文档模板
├── phase1/                     # Phase 1 需求
│   ├── feature-auth.md
│   └── feature-upload.md
├── phase2/                     # Phase 2 需求
│   └── feature-reader.md
└── phase3/                     # Phase 3 需求
    └── feature-xxx.md
```

### 需求文档状态

| 状态 | 说明 | 图标 |
|------|------|------|
| `pending` | 待处理 | 📝 |
| `developing` | 开发中 | 🚧 |
| `done` | 已完成 | ✅ |

### 版本规划流程

1. **规划阶段**：确定版本目标，创建阶段目录
2. **需求收集**：在对应阶段目录下创建需求文档
3. **开发实施**：按需求优先级开发，更新状态
4. **版本发布**：所有需求完成后，标记版本完成

### ✅ 规则速查

- ✅ 需求编号必须包含阶段前缀：`REQ-P1-001`
- ✅ 需求文档必须放在对应阶段目录下
- ✅ 需求索引必须按阶段分组显示
- ❌ 禁止跨阶段混合需求编号

## 7. 进度跟踪规范

### 核心原则

每次开发任务完成后，**必须**更新项目进度记录，确保下次新对话能无缝接续。

### Memory 文件命名规范

新建 memory 文件时，使用 **数字前缀 + kebab-case**：

```
01_project-overview.md        # 按创建时间编号
02_rules-spec-system.md
03_ngrok-setup.md
04_current-progress.md
05_frontend-standards-refactor.md
06_xxx.md                     # 后续新文件按序号递增
```

- 数字按创建时间先后分配
- 文件名用 kebab-case（小写 + 连字符）
- 创建后同步更新 `MEMORY.md` 索引

### 需要更新的文件

| 文件 | 更新内容 | 触发时机 |
|------|----------|----------|
| `memory/current-progress.md` | 已完成 / 进行中 / 待开始 的勾选状态 | 每完成一个功能 |
| `docs/requirements/feature-*.md` | 状态标签（pending→developing→done） | 功能状态变更时 |
| `docs/requirements/feature-*.md` | 技术实现要点 checkbox | 每完成一个实现点 |

### 更新格式

#### memory/current-progress.md

将已完成项从 `[ ]` 改为 `[x]`，必要时新增条目：

```markdown
## 已完成
- [x] 功能A 已完成
- [x] 新增：功能B

## 进行中
- [ ] 功能C（当前进度描述）

## 待开始
- [ ] 功能D
```

#### 需求文档状态标签

```markdown
> **状态**: 📝 pending | 🚧 developing | ✅ done
```

### ✅ 规则速查

- ✅ 每完成一个功能后，必须更新 `memory/current-progress.md`
- ✅ 功能状态变更时，必须更新对应需求文档的状态标签
- ✅ 新建 memory 文件后，必须更新 `MEMORY.md` 索引
- ❌ 禁止忘记更新进度记录（会导致下次会话无法接续）

---

*本文件由 AI 维护，请勿手动编辑*

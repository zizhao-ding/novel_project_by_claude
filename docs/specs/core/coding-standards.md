# 编码规范 (Coding Standards)

> **优先级**: P0 - 必须遵守
> **最后更新**: 2026-06-25

## 1. 项目结构 & 文件命名

### 目录结构

```
src/
├── assets/          # 静态资源（图片、图标、字体、全局样式）
├── components/      # 公共组件
│   ├── base/        #   基础组件（Button, Input, Modal 等通用封装）
│   ├── business/    #   业务组件（NovelCard, UploadPanel 等）
│   └── ui/          #   UI 组件（布局、容器等）
├── views/           # 页面视图组件（每个路由对应一个视图）
├── router/          # 路由配置
├── stores/          # Pinia 状态管理
├── services/        # API 服务层（HTTP 请求封装）
├── composables/     # Vue Composables（可复用逻辑）
├── utils/           # 纯工具函数
├── types/           # TypeScript 类型定义
├── directives/      # Vue 自定义指令
├── plugins/         # Vue 插件
└── constants/       # 常量定义
```

### 文件命名规范

| 文件类型 | 命名方式 | 示例 |
|----------|----------|------|
| Vue 组件 | **PascalCase** | `UserCard.vue`, `NovelReader.vue` |
| JS/TS 工具 | **kebab-case** | `api-client.ts`, `format-date.ts` |
| 样式文件 | **kebab-case** | `variables.scss`, `common.scss` |
| 类型定义 | **kebab-case** | `novel.ts`, `user.ts` |
| 测试文件 | `*.spec.ts` | `user-card.spec.ts` |
| Store 文件 | 名词单数 | `user.ts`, `novel.ts`（非 `users.ts`） |
| 视图文件 | 以 `View` 结尾 | `HomeView.vue`, `LibraryView.vue` |

### ✅ 正确 vs ❌ 错误

```typescript
// ✅ 组件导入使用 @ 别名
import UserCard from '@/components/base/UserCard.vue';

// ✅ 工具函数导入
import { formatDate } from '@/utils/format-date';

// ❌ 禁止使用相对路径跨层级导入
import UserCard from '../../../components/UserCard.vue';

// ❌ 禁止组件使用 kebab-case 命名
// ❌ user-card.vue
```

## 2. Vue 3 组件开发规范

### 核心原则

1. **强制使用 `<script setup lang="ts">`** — 所有组件使用 Composition API 语法糖
2. **Props 使用 TypeScript 接口定义** — 配合 `withDefaults` 设置默认值
3. **Emits 使用类型声明** — 自定义事件使用 kebab-case
4. **事件处理函数使用 `handle` 前缀**

### 组件标准模板

```vue
<template>
  <div class="component-name">
    <!-- 模板中避免复杂表达式，使用 computed -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { PropType } from 'vue';

// Props 定义
interface Props {
  title: string;
  disabled?: boolean;
  items?: Item[];
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  items: () => [],
});

// Emits 定义（自定义事件使用 kebab-case）
const emits = defineEmits<{
  (e: 'item-click', id: number): void;
  (e: 'value-change', value: string): void;
}>();

// 响应式状态
const internalValue = ref('');

// Computed（模板中的复杂逻辑放这里）
const isValid = computed(() => internalValue.value.length > 0);

// 方法（事件处理使用 handle 前缀）
function handleChange(value: string) {
  internalValue.value = value;
  emits('value-change', value);
}

// 生命周期
onMounted(() => {
  // 初始化逻辑
});
</script>

<style scoped lang="scss">
.component-name {
  // BEM 命名
}
</style>
```

### Props 规范

```typescript
// ✅ 复杂类型使用 PropType + 接口
interface NovelData {
  id: number;
  title: string;
  content: string;
}

const props = defineProps({
  novel: {
    type: Object as PropType<NovelData>,
    required: true,
  },
});

// ❌ 禁止使用 Options API 的 props 数组写法
// props: ['title', 'content']
```

### 事件规范

| 类型 | 命名方式 | 示例 |
|------|----------|------|
| DOM 事件 | Vue 默认 | `@click`, `@input`, `@keydown` |
| 自定义事件 | kebab-case | `@item-click`, `@value-change` |
| 处理函数 | `handle` + PascalCase | `handleClick`, `handleInputChange` |

### ❌ 禁止事项

- ❌ 禁止使用 Options API（`data()`, `methods`, `computed` 选项）
- ❌ 禁止在模板中使用复杂表达式（抽取为 `computed`）
- ❌ 禁止直接操作 DOM（使用 `ref` + `v-model` / 响应式绑定）
- ❌ 禁止 `v-for` 缺少 `:key`

## 3. TypeScript 类型规范

### 核心约束

**所有新代码必须使用 TypeScript。** `.vue` 文件使用 `<script setup lang="ts">`，工具文件使用 `.ts` 扩展名。

### 命名规范

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

### 泛型规范

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

### 类型文件组织

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

### ✅ 正确 vs ❌ 错误

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

## 4. 样式 & CSS 规范

### 技术方案

**UnoCSS**（原子化 CSS）+ **SCSS**（自定义样式，BEM 命名）+ **Element Plus CSS 变量**。

### BEM 命名规范

```scss
// Block（块）
.user-card {
  padding: 16px;
  border: 1px solid var(--el-border-color);
  border-radius: 8px;

  // Element（元素）— 使用 __ 连接
  &__header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }

  &__avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
  }

  &__content {
    flex: 1;
  }

  // Modifier（修饰符）— 使用 -- 连接
  &--featured {
    border-color: var(--el-color-primary);
    box-shadow: 0 0 8px rgba(var(--el-color-primary-rgb), 0.2);
  }

  &--disabled {
    opacity: 0.5;
    pointer-events: none;
  }
}
```

### Element Plus CSS 变量

```scss
// ✅ 使用 Element Plus CSS 变量，保持主题统一
.custom-component {
  color: var(--el-color-primary);
  background: var(--el-bg-color);
  border-color: var(--el-border-color);

  &:hover {
    color: var(--el-color-primary-light-3);
  }
}
```

### SCSS 文件组织

```scss
// styles/variables.scss — 项目级变量
$primary-color: #409eff;
$text-color: #303133;
$border-color: #dcdfe6;
$sidebar-width: 240px;

// styles/mixins.scss — 可复用 Mixin
@mixin text-ellipsis($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

### 样式作用域

```vue
<!-- ✅ 组件样式使用 scoped -->
<style scoped lang="scss">
.component { }
</style>

<!-- ✅ 全局样式放在 src/assets/styles/ 下 -->
<!-- ❌ 避免在组件中写非 scoped 样式 -->
```

### ✅ 推荐 vs ❌ 避免

- ✅ 优先使用 UnoCSS 原子类（`flex`, `p-4`, `text-center`）
- ✅ 复杂样式使用 BEM + SCSS
- ✅ 颜色/间距使用 Element Plus CSS 变量
- ❌ 禁止内联样式（`style="color: red"`）
- ❌ 禁止使用 `!important`（除非覆盖第三方库样式）
- ❌ 禁止使用 ID 选择器（`#app` 除外）

## 5. Git 提交 & 分支规范

### 分支策略

```
main                    # 生产分支（只接受 merge，不直接 commit）
├── feature_1.0.0.1     # 版本集成分支
│   ├── feature_zizhao  # 个人功能分支（当前分支）
│   └── feature_xxx     # 其他功能分支
```

### Commit 规范（Conventional Commits）

```
<type>(<scope>): <subject>
```

#### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(novel): 添加小说上传组件` |
| `fix` | Bug 修复 | `fix(reader): 修复翻页时内容丢失` |
| `docs` | 文档变更 | `docs(rules): 添加组件开发规范` |
| `style` | 代码格式 | `style: 统一缩进为2空格` |
| `refactor` | 重构 | `refactor(api): 重构请求拦截器` |
| `perf` | 性能优化 | `perf(list): 添加虚拟滚动` |
| `test` | 测试相关 | `test(store): 添加 novel store 测试` |
| `chore` | 构建/工具 | `chore: 添加 ESLint 配置` |

#### Scope 范围

常用：`auth`, `novel`, `reader`, `library`, `upload`, `router`, `store`, `api`, `style`, `rules`, `spec`

#### 示例

```bash
# ✅ 好的 commit
git commit -m "feat(novel): 添加小说列表分页功能"
git commit -m "fix(reader): 修复页面刷新后阅读位置丢失"

# ❌ 不好的 commit
git commit -m "update code"
git commit -m "修改了一些东西"
git commit -m "WIP"
```

### 工作流程

1. 从集成分支创建个人功能分支
2. 在个人分支上开发，保持小步提交
3. 完成后发起 PR 合并到集成分支
4. 代码审查通过后合并

### ✅ 规则速查

- ✅ Commit message 使用英文简要描述
- ✅ 一个 commit 只做一件事
- ✅ 提交前确保代码可以运行
- ❌ 禁止 `git push --force` 到共享分支
- ❌ 禁止提交 `console.log` 调试代码

---

*本文件由 AI 维护，请勿手动编辑*

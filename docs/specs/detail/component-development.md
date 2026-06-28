# 组件开发详细指南

> **优先级**: P1 - 应该遵守
> **最后更新**: 2026-06-28
> **基于**: AppHeader.vue, NovelCard.vue 等实际组件模式

## 1. 组件文件结构

```
src/components/
├── AppHeader.vue      # 全局组件（PascalCase 命名）
├── NovelCard.vue       # 业务组件
└── ...
```

### 标准模板

```vue
<script setup lang="ts">
// 1. 导入
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useUserStore } from '@/stores/user';

// 2. Props（TypeScript 纯类型）
interface Props {
  title: string;
  showSearch?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  showSearch: true,
});

// 3. Emits（TypeScript 元组）
const emit = defineEmits<{
  (e: 'search', query: string): void;
  (e: 'back'): void;
}>();

// 4. Store / Router
const router = useRouter();
const userStore = useUserStore();

// 5. 本地状态
const searchQuery = ref('');

// 6. 计算属性
const displayTitle = computed(() => props.title || '默认标题');

// 7. 方法
function handleSearch() {
  emit('search', searchQuery.value);
}
</script>

<template>
  <div class="component-name">
    <!-- 模板 -->
  </div>
</template>

<style scoped lang="scss">
.component-name {
  // BEM 命名

  &__child {
    // 子元素
  }

  &--modifier {
    // 修饰符
  }
}
</style>
```

## 2. Props 规范

### ✅ 正确

```typescript
// 纯类型接口定义
interface Props {
  novelId: number;
  showActions?: boolean;
  colorIndex?: number;
}
const props = withDefaults(defineProps<Props>(), {
  showActions: true,
  colorIndex: 0,
});
```

### ❌ 错误

```typescript
// 运行时对象（禁止）
defineProps({
  novelId: { type: Number, required: true },
});
```

## 3. Emits 规范

```typescript
// ✅ TypeScript 元组签名
const emit = defineEmits<{
  (e: 'click', id: number): void;
  (e: 'delete', id: number, title: string): void;
}>();

// ❌ 运行时数组（禁止）
defineEmits(['click', 'delete']);
```

## 4. 样式规范

### BEM 命名规则

```scss
.novel-card {              // Block（组件根元素，kebab-case）
  padding: 16px;

  &__cover {               // Element（子元素，双下划线）
    width: 120px;
  }

  &__title {               // Element
    font-size: 16px;
  }

  &--selected {            // Modifier（修饰符，双连字符）
    border-color: #409eff;
  }
}
```

### Scoped + SCSS 组合

```vue
<!-- ✅ 组件样式用 scoped -->
<style scoped lang="scss">
.novel-card { ... }
</style>

<!-- ⚠️ Element Plus 覆盖用非 scoped（谨慎使用） -->
<style lang="scss">
.el-popover.user-popover {
  padding: 0;
}
</style>
```

## 5. 模板规范

### 条件渲染

```vue
<!-- ✅ 使用 v-if/v-else-if/v-else -->
<div v-if="loading" class="loading-state">
  <el-icon class="is-loading"><Loading /></el-icon>
  <span>加载中...</span>
</div>
<div v-else-if="error" class="error-state">
  <el-result icon="error" :title="error" />
</div>
<div v-else-if="!items.length" class="empty-state">
  <el-empty description="暂无数据" />
</div>
<div v-else class="data-grid">
  <!-- 数据展示 -->
</div>
```

### 列表渲染

```vue
<!-- ✅ 必须提供唯一 key -->
<div v-for="novel in novels" :key="novel.id" class="novel-card">
  <NovelCard :novel="novel" />
</div>
```

### 事件绑定

```vue
<!-- ✅ 简短方法调用 -->
<el-button @click="handleDelete(novel.id)">删除</el-button>

<!-- ❌ 禁止模板内复杂表达式 -->
<el-button @click="novels.filter(n => n.id !== id).forEach(...)">
```

## 6. 工具函数

### 避免重复定义

`formatSize`、`formatDate` 等工具函数在多处重复定义。应放在 `src/utils/`：

```typescript
// utils/format.ts
export function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('zh-CN');
}
```

## 7. 组件通信

| 场景 | 方式 |
|------|------|
| 父→子 | Props |
| 子→父 | Emits |
| 跨层级 | Pinia Store |
| 路由参数 | `useRoute().params` / `props: true` |
| 全局通知 | `ElMessage` |

## 8. 关键约束速查

- ✅ 使用 `<script setup lang="ts">`
- ✅ Props 使用 TypeScript 纯类型 + `withDefaults`
- ✅ Emits 使用 TypeScript 元组签名
- ✅ 样式使用 scoped SCSS + BEM 命名
- ✅ 模板中处理 loading/empty/error 三态
- ✅ 工具函数集中在 `utils/`，避免重复
- ❌ 禁止 Options API
- ❌ 禁止模板内复杂表达式
- ❌ 禁止直接操作 DOM

# 02 — Vue 3 组件开发规范

## 核心原则

1. **强制使用 `<script setup lang="ts">`** — 所有组件使用 Composition API 语法糖
2. **Props 使用 TypeScript 接口定义** — 配合 `withDefaults` 设置默认值
3. **Emits 使用类型声明** — 自定义事件使用 kebab-case
4. **事件处理函数使用 `handle` 前缀**

## 组件标准模板

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

## Props 规范

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

## 事件规范

| 类型 | 命名方式 | 示例 |
|------|----------|------|
| DOM 事件 | Vue 默认 | `@click`, `@input`, `@keydown` |
| 自定义事件 | kebab-case | `@item-click`, `@value-change` |
| 处理函数 | `handle` + PascalCase | `handleClick`, `handleInputChange` |

## ❌ 禁止事项

- ❌ 禁止使用 Options API（`data()`, `methods`, `computed` 选项）
- ❌ 禁止在模板中使用复杂表达式（抽取为 `computed`）
- ❌ 禁止直接操作 DOM（使用 `ref` + `v-model` / 响应式绑定）
- ❌ 禁止 `v-for` 缺少 `:key`

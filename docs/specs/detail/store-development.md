# Store 开发详细指南

> **优先级**: P1 - 应该遵守
> **最后更新**: 2026-06-28
> **基于**: stores/user.ts, reader.ts, novel.ts 等实际 Store 模式

## 1. Setup Store 标准模板

```typescript
// stores/example.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import type { Example } from '@/types/example';
import { exampleApi } from '@/services/example';

export const useExampleStore = defineStore('example', () => {
  // ═══════════════════════════════════════════
  // State
  // ═══════════════════════════════════════════
  const items = ref<Example[]>([]);
  const currentItem = ref<Example | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // ═══════════════════════════════════════════
  // Getters (Computed)
  // ═══════════════════════════════════════════
  const itemCount = computed(() => items.value.length);
  const activeItems = computed(() =>
    items.value.filter(i => i.status === 'active')
  );

  // ═══════════════════════════════════════════
  // Actions
  // ═══════════════════════════════════════════
  async function fetchAll() {
    loading.value = true;
    error.value = null;
    try {
      const response = await exampleApi.getList();
      items.value = (response as any).data?.items ?? [];
    } catch (err) {
      error.value = (err as Error).message;
      ElMessage.error('加载失败');
    } finally {
      loading.value = false;
    }
  }

  async function create(data: FormData) {
    try {
      const response = await exampleApi.create(data);
      const item = (response as any).data;
      items.value.unshift(item);
      ElMessage.success('创建成功');
      return item;
    } catch (err) {
      ElMessage.error('创建失败');
      throw err;
    }
  }

  async function remove(id: number) {
    try {
      await exampleApi.delete(id);
      items.value = items.value.filter(i => i.id !== id);
      ElMessage.success('删除成功');
    } catch (err) {
      ElMessage.error('删除失败');
      throw err;
    }
  }

  function clearError() {
    error.value = null;
  }

  // ═══════════════════════════════════════════
  // Return
  // ═══════════════════════════════════════════
  return {
    // State
    items, currentItem, loading, error,
    // Getters
    itemCount, activeItems,
    // Actions
    fetchAll, create, remove, clearError,
  };
});
```

## 2. API 响应类型断言

所有 API 遵循 `{ code: number, message: string, data: T }` 格式，code=0 表示成功：

```typescript
// ✅ 标准类型断言
const response = await novelApi.getList();
items.value = (response as any).data?.items ?? [];

// ✅ 对于确认型响应
await exampleApi.delete(id);
// 成功则继续，失败由 catch 处理
```

## 3. 组件中使用 Store

```vue
<script setup lang="ts">
import { useExampleStore } from '@/stores/example';
import { storeToRefs } from 'pinia';

const store = useExampleStore();
// ✅ State/Getter 使用 storeToRefs 保持响应性
const { items, loading, itemCount } = storeToRefs(store);
// ✅ Actions 直接解构
const { fetchAll, create, remove } = store;

onMounted(() => {
  fetchAll();
});
</script>
```

## 4. 错误处理模式

```typescript
// 模式 A：Store Action 中统一处理（推荐）
async function doSomething() {
  loading.value = true;
  error.value = null;
  try {
    // ... API 调用
    ElMessage.success('成功');
  } catch (err) {
    error.value = (err as Error).message;
    ElMessage.error(`失败：${error.value}`);
    throw err; // 重新抛出，让调用方也能感知
  } finally {
    loading.value = false;
  }
}

// 模式 B：ViewModel 层处理确认弹窗
// Store 只管理数据，确认弹窗在视图中
// ✅ Store Action 不调用 ElMessageBox（UI 组件）
```

## 5. 持久化存储

```typescript
// 使用 @vueuse/core 的 useLocalStorage
import { useLocalStorage } from '@vueuse/core';

const settings = useLocalStorage('reader-settings', {
  theme: 'light' as 'light' | 'dark' | 'sepia',
  fontSize: 16,
});
```

## 6. 乐观更新

```typescript
// 先调用 API，成功后再更新本地状态
async function batchRemove(novelIds: number[]) {
  try {
    await bookshelfApi.batchRemove(novelIds);
    // API 成功后同步本地
    items.value = items.value.filter(i => !novelIds.includes(i.id));
    ElMessage.success('移除成功');
  } catch (err) {
    ElMessage.error('移除失败');
    throw err;
  }
}
```

## 7. Store 命名规范

| 类别 | 命名 | 示例 |
|------|------|------|
| Store ID | 小写名词 | `'user'`, `'novel'`, `'reader'` |
| Store 函数 | `use` + PascalCase + `Store` | `useUserStore` |
| State | 名词 | `novels`, `loading`, `error` |
| Getter | 名词/形容词 | `novelCount`, `isAuthenticated` |
| Action | 动词 | `fetchNovels`, `addNovel` |

## 8. 关键约束速查

- ✅ 必须使用 `defineStore` Setup Store 模式
- ✅ State/Getter 解构必须用 `storeToRefs`
- ✅ 所有异步 Action 必须 try-catch
- ✅ 捕获错误必须给用户提示（ElMessage）
- ✅ Store 只管理数据，UI 确认弹窗在视图层
- ❌ 禁止 Options Store
- ❌ 禁止在 Store 中调用 ElMessageBox（UI 耦合）
- ❌ 禁止直接修改 State（必须通过 Action）
- ❌ 禁止吞掉错误（空 catch 块）

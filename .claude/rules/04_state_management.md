# 04 — Pinia 状态管理规范

## 核心原则

1. **使用 Setup Store 模式**（`defineStore('name', () => { ... })`），禁止 Options Store
2. **Store 文件放在 `src/stores/`**，一个 store 一个文件
3. **组件中使用 `storeToRefs` 解构**以保持响应性

## Store 标准模板

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

## Store 使用规范

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

## 命名约定

| 类别 | 命名方式 | 示例 |
|------|----------|------|
| Store 文件名 | 名词单数 | `user.ts`, `novel.ts` |
| Store 实例 | `use` + 名词 + `Store` | `useUserStore`, `useNovelStore` |
| State | 名词 | `novels`, `loading`, `error` |
| Getter | 名词/形容词 | `novelCount`, `isAuthenticated` |
| Action | 动词 | `fetchNovels`, `addNovel`, `removeNovel` |

## ❌ 禁止事项

- ❌ 禁止使用 Options Store（`state: () => ({...})`）
- ❌ 禁止直接修改 state（必须通过 action）
- ❌ 禁止解构 state 时不用 `storeToRefs`（会丢失响应性）

<template>
  <div class="search-page">
    <AppHeader />

    <main class="search-page__main">
      <div class="search-page__input-row">
        <el-input v-model="keyword" placeholder="输入小说名称搜索..." size="large" clearable @keyup.enter="doSearch">
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" size="large" @click="doSearch">搜索</el-button>
      </div>

      <div v-if="hasSearched" class="search-page__result">
        <p class="search-page__result-count">共找到 {{ total }} 本相关小说</p>

        <div v-if="total === 0" class="search-page__empty">
          <el-empty description="未找到相关小说，换个关键词试试" />
        </div>

        <div v-else v-loading="loading" class="search-page__list">
          <div v-for="item in results" :key="item.id" class="search-page__item">
            <div class="search-page__item-cover" :style="{ backgroundColor: getColor(item.id) }">
              {{ item.title.charAt(0) }}
            </div>
            <div class="search-page__item-body">
              <div class="search-page__item-title">{{ item.title }}</div>
              <div class="search-page__item-meta">
                <el-tag v-if="item.category_name" size="small" type="info">{{ item.category_name }}</el-tag>
                <span>{{ formatSize(item.file_size) }}</span>
              </div>
            </div>
            <el-button type="primary" size="small" @click="$router.push({ path: `/reader/${item.id}`, query: { title: item.title } })"
              >开始阅读</el-button
            >
          </div>
        </div>

        <div v-if="total > pageSize" class="search-page__pagination">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="total"
            layout="prev, pager, next"
            @current-change="doSearch"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Search } from '@element-plus/icons-vue';
import { searchApi } from '../services/search';
import AppHeader from '../components/AppHeader.vue';

const route = useRoute();
const keyword = ref('');
const results = ref<
  Array<{
    id: number;
    title: string;
    file_size: number;
    category_id: number | null;
    category_name: string | null;
    visibility: string;
    created_at: string;
  }>
>([]);
const total = ref(0);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const hasSearched = ref(false);

const COLORS = ['#e74c3c', '#3498db', '#2c3e50', '#f39c12', '#27ae60', '#8e44ad', '#e67e22', '#1abc9c'];
function getColor(id: number) {
  return COLORS[id % COLORS.length];
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function doSearch() {
  const kw = keyword.value.trim();
  if (!kw) return;
  loading.value = true;
  hasSearched.value = true;
  try {
    const response = await searchApi.search(kw, currentPage.value, pageSize.value);
    const res = response as unknown as {
      code: number;
      data: { items: typeof results.value; total: number; page: number; page_size: number };
    };
    if (res.code === 0 && res.data) {
      results.value = res.data.items;
      total.value = res.data.total;
    }
  } catch {
    total.value = 0;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  const q = route.query.q as string;
  if (q) {
    keyword.value = q;
    doSearch();
  }
});
</script>

<style scoped lang="scss">
.search-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);
  padding-top: 56px;

  &__main {
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 24px;
  }

  &__input-row {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
  }

  &__result-count {
    font-size: 14px;
    color: var(--el-text-color-secondary);
    margin-bottom: 16px;
  }

  &__empty {
    padding: 40px 0;
  }

  &__list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  &__item {
    display: flex;
    align-items: center;
    gap: 16px;
    background: #fff;
    padding: 16px;
    border-radius: 10px;
  }

  &__item-cover {
    width: 60px;
    height: 80px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.85);
    font-size: 28px;
    font-weight: 700;
    flex-shrink: 0;
  }

  &__item-body {
    flex: 1;
  }

  &__item-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
  }

  &__item-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--el-text-color-secondary);
  }

  &__pagination {
    margin-top: 24px;
    display: flex;
    justify-content: center;
  }
}
</style>

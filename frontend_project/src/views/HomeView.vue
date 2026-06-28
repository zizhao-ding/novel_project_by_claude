<template>
  <div class="home-page">
    <AppHeader />

    <main class="home-page__main">
      <!-- 欢迎区（未登录） -->
      <div v-if="!userStore.isAuthenticated" class="home-page__hero">
        <h2>欢迎来到小说阅读平台</h2>
        <p>海量 TXT 小说，随时随地在线阅读</p>
      </div>

      <!-- 热门推荐 -->
      <section class="home-page__section">
        <h3 class="home-page__section-title">🔥 热门推荐</h3>
        <div v-if="homeStore.loading" class="home-page__loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        </div>
        <div v-else-if="homeStore.hotNovels.length === 0" class="home-page__empty">
          <el-empty description="暂无推荐" />
        </div>
        <div v-else class="home-page__card-row">
          <NovelCard
            v-for="(novel, idx) in homeStore.hotNovels"
            :key="novel.id"
            :title="novel.title"
            :file-size="novel.file_size"
            :subtitle="novel.bookshelf_count ? `${novel.bookshelf_count} 人收藏` : undefined"
            :color-index="idx"
            @click="$router.push({ path: `/reader/${novel.id}`, query: { title: novel.title } })"
          />
        </div>
      </section>

      <!-- 分类浏览 -->
      <section class="home-page__section">
        <h3 class="home-page__section-title">📂 分类浏览</h3>
        <div class="home-page__tags">
          <el-tag
            v-for="cat in categories"
            :key="cat"
            class="home-page__tag"
            size="large"
            effect="plain"
            @click="$router.push(`/library?category=${encodeURIComponent(cat)}`)"
          >
            {{ cat }}
          </el-tag>
        </div>
      </section>

      <!-- 最新上传 -->
      <section class="home-page__section">
        <h3 class="home-page__section-title">🆕 最近更新</h3>
        <div v-if="homeStore.loading" class="home-page__loading">
          <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        </div>
        <div v-else-if="homeStore.latestNovels.length === 0" class="home-page__empty">
          <el-empty description="暂无小说" />
        </div>
        <div v-else class="home-page__card-row">
          <NovelCard
            v-for="(novel, idx) in homeStore.latestNovels"
            :key="novel.id"
            :title="novel.title"
            :file-size="novel.file_size"
            :color-index="idx + 4"
            @click="$router.push({ path: `/reader/${novel.id}`, query: { title: novel.title } })"
          />
        </div>
      </section>

      <!-- 底部 -->
      <footer class="home-page__footer">
        <router-link to="/help">帮助中心</router-link>
        <span>小说阅读平台 v1.0.0</span>
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { Loading } from '@element-plus/icons-vue';
import { useUserStore } from '../stores/user';
import { useHomeStore } from '../stores/home';
import AppHeader from '../components/AppHeader.vue';
import NovelCard from '../components/NovelCard.vue';

const userStore = useUserStore();
const homeStore = useHomeStore();

const categories = ['玄幻', '仙侠', '都市', '科幻', '历史', '游戏', '奇幻', '悬疑'];

onMounted(() => {
  homeStore.fetchAll();
});
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);
  padding-top: 56px;

  &__main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 32px 24px;
  }

  &__hero {
    text-align: center;
    padding: 60px 0 40px;
    h2 {
      font-size: 28px;
      margin: 0 0 12px;
    }
    p {
      font-size: 16px;
      color: var(--el-text-color-secondary);
    }
  }

  &__section {
    margin-bottom: 36px;

    &-title {
      font-size: 18px;
      font-weight: 600;
      margin: 0 0 16px;
    }
  }

  &__card-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  &__tags {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }

  &__tag {
    cursor: pointer;
    &:hover {
      transform: translateY(-2px);
    }
  }

  &__loading {
    display: flex;
    justify-content: center;
    padding: 40px 0;
    color: var(--el-text-color-placeholder);
  }

  &__empty {
    padding: 20px 0;
  }

  &__footer {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 24px;
    padding: 32px 0 16px;
    font-size: 13px;
    color: var(--el-text-color-placeholder);
    a {
      color: var(--el-text-color-secondary);
      text-decoration: none;
      &:hover {
        color: var(--el-color-primary);
      }
    }
  }
}
</style>

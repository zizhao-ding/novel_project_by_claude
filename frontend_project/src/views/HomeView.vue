<template>
  <div class="home-page">
    <header class="home-page__header">
      <h1 class="home-page__logo">📖 小说阅读平台</h1>
      <nav class="home-page__nav">
        <template v-if="userStore.isAuthenticated">
          <span class="home-page__username">{{ userStore.user?.username }}</span>
          <el-button type="danger" text @click="handleLogout">退出登录</el-button>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-button type="primary">登录</el-button>
          </router-link>
          <router-link to="/register">
            <el-button text>注册</el-button>
          </router-link>
        </template>
      </nav>
    </header>

    <main class="home-page__main">
      <div class="home-page__hero">
        <h2>欢迎使用小说阅读平台</h2>
        <p>上传你的 TXT 小说，随时随地在线阅读</p>
        <div class="home-page__actions">
          <router-link to="/library">
            <el-button type="primary" size="large">进入书房</el-button>
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';

const router = useRouter();
const userStore = useUserStore();

async function handleLogout() {
  const confirmed = await userStore.logout();
  if (confirmed) {
    router.push('/');
  }
}
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  background: var(--el-bg-color);

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 32px;
    background: #fff;
    border-bottom: 1px solid var(--el-border-color-light);
  }

  &__logo {
    font-size: 20px;
    margin: 0;
  }

  &__nav {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__username {
    font-size: 14px;
    color: var(--el-text-color-secondary);
  }

  &__main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 65px);
  }

  &__hero {
    text-align: center;

    h2 {
      font-size: 32px;
      color: var(--el-text-color-primary);
      margin-bottom: 12px;
    }

    p {
      font-size: 16px;
      color: var(--el-text-color-secondary);
      margin-bottom: 32px;
    }
  }

  &__actions {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
}
</style>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <!-- 左侧: 返回区 -->
      <div class="app-header__left">
        <div v-if="showBack" class="app-header__back-area" @click="goBack">
          <el-icon :size="18"><ArrowLeft /></el-icon>
          <span class="app-header__back-title">{{ pageTitle }}</span>
        </div>
        <router-link v-else to="/" class="app-header__logo">📖 小说阅读平台</router-link>
      </div>

      <!-- 中间: 搜索 -->
      <div class="app-header__center">
        <el-input v-model="searchText" placeholder="搜索小说..." size="default" class="app-header__search" @keyup.enter="doSearch">
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <!-- 右侧: 用户区 -->
      <div class="app-header__right">
        <template v-if="userStore.isAuthenticated">
          <router-link to="/library" class="app-header__nav-link">书房</router-link>
          <router-link v-if="canUpload()" to="/upload" class="app-header__nav-link">上传</router-link>
          <el-popover placement="bottom-end" :width="220" trigger="hover" popper-class="user-popover">
            <template #reference>
              <div class="app-header__avatar" :style="{ backgroundColor: userStore.user?.avatar || '#409EFF' }">
                {{ avatarLetter }}
              </div>
            </template>
            <div class="user-popover__card">
              <div class="user-popover__avatar" :style="{ backgroundColor: userStore.user?.avatar || '#409EFF' }">
                {{ avatarLetter }}
              </div>
              <div class="user-popover__name">{{ userStore.user?.username }}</div>
              <el-tag :type="roleTagType" size="small" effect="dark">{{ roleLabel }}</el-tag>
              <el-divider style="margin: 12px 0" />
              <div class="user-popover__links">
                <div class="user-popover__link" @click="$router.push('/library')">📚 我的书房</div>
                <div class="user-popover__link" @click="$router.push('/user')">👤 个人中心</div>
                <div v-if="isAdmin" class="user-popover__link" @click="$router.push('/admin/users')">⚙️ 用户管理</div>
                <div class="user-popover__link" @click="$router.push('/help')">❓ 帮助中心</div>
                <div class="user-popover__link user-popover__link--danger" @click="handleLogout">🚪 退出登录</div>
              </div>
            </div>
          </el-popover>
        </template>
        <template v-else>
          <router-link to="/login"><el-button size="small">登录</el-button></router-link>
          <router-link to="/register"><el-button size="small" type="primary">注册</el-button></router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ArrowLeft, Search } from '@element-plus/icons-vue';
import { useUserStore } from '../stores/user';
import { usePermission } from '../composables/usePermission';
import type { UserRole } from '../types/user';
import { ROLE_LABELS } from '../types/user';

const _props = defineProps<{ showBack?: boolean; pageTitle?: string }>();

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const { isAdmin, canUpload } = usePermission();

const searchText = ref((route.query.q as string) || '');

const avatarLetter = computed(() => (userStore.user?.username || 'U').charAt(0).toUpperCase());
const roleLabel = computed(() => ROLE_LABELS[(userStore.user?.role || 'member') as UserRole] || '普通成员');
const roleTagType = computed(() => {
  const role = userStore.user?.role;
  if (role === 'admin') return 'danger';
  if (role === 'seed_member') return 'warning';
  return 'info';
});

function goBack() {
  router.back();
}

function doSearch() {
  const kw = searchText.value.trim();
  if (kw) {
    router.push({ path: '/search', query: { q: kw } });
  }
}

async function handleLogout() {
  await userStore.logout();
  router.push('/');
}
</script>

<style lang="scss">
.user-popover {
  padding: 0 !important;
}
</style>

<style scoped lang="scss">
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 56px;
  background: #fff;
  border-bottom: 1px solid var(--el-border-color-light);
  display: flex;
  align-items: center;

  &__inner {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0 24px;
    gap: 24px;
  }

  &__left {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  &__back-area {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: var(--el-text-color-primary);
    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__back-title {
    font-size: 15px;
    font-weight: 500;
  }

  &__logo {
    font-size: 18px;
    font-weight: 700;
    color: var(--el-text-color-primary);
    text-decoration: none;
  }

  &__center {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  &__search {
    max-width: 360px;
  }

  &__right {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-shrink: 0;
    margin-left: auto;
  }

  &__nav-link {
    font-size: 14px;
    color: var(--el-text-color-regular);
    text-decoration: none;
    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 15px;
    cursor: pointer;
    transition: transform 0.2s;
    &:hover {
      transform: scale(1.1);
    }
  }
}

.user-popover {
  &__card {
    padding: 16px;
    text-align: center;
  }

  &__avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 24px;
    margin: 0 auto 8px;
  }

  &__name {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
  }

  &__links {
    text-align: left;
  }

  &__link {
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 6px;
    font-size: 14px;
    transition: background 0.2s;
    &:hover {
      background: var(--el-fill-color-light);
    }
    &--danger {
      color: var(--el-color-danger);
    }
  }
}
</style>

<template>
  <div class="user-page">
    <!-- 顶部导航栏 -->
    <header class="user-page__header">
      <div class="user-page__header-left">
        <router-link to="/library" class="user-page__back">
          <el-icon><ArrowLeft /></el-icon>
        </router-link>
        <h1 class="user-page__title">我的</h1>
      </div>
    </header>

    <!-- 用户信息卡片 -->
    <div class="user-page__profile">
      <div class="user-page__avatar-section">
        <el-avatar :size="80" :src="userAvatar" :style="{ backgroundColor: avatarColor }" class="user-page__avatar">
          {{ avatarText }}
        </el-avatar>
        <div class="user-page__user-info">
          <h2 class="user-page__username">{{ user?.username || '未登录' }}</h2>
          <el-tag :type="roleTagType" size="small" effect="dark" class="user-page__role-tag">
            {{ roleLabel }}
          </el-tag>
        </div>
      </div>
      <div class="user-page__join-date">
        <el-icon><Calendar /></el-icon>
        <span>加入于 {{ formatDate(user?.created_at) }}</span>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="user-page__stats">
      <div class="stat-card" @click="router.push('/library')">
        <div class="stat-card__value">{{ stats.bookshelf_count }}</div>
        <div class="stat-card__label">书架藏书</div>
      </div>
      <div class="stat-card">
        <div class="stat-card__value">{{ stats.novel_count }}</div>
        <div class="stat-card__label">上传小说</div>
      </div>
      <div class="stat-card">
        <div class="stat-card__value">{{ stats.category_count }}</div>
        <div class="stat-card__label">自建分类</div>
      </div>
      <div class="stat-card">
        <div class="stat-card__value">{{ formatSize(stats.total_size) }}</div>
        <div class="stat-card__label">存储空间</div>
      </div>
    </div>

    <!-- 功能菜单 -->
    <div class="user-page__menu">
      <div class="menu-group">
        <div class="menu-group__title">内容管理</div>
        <div class="menu-item" @click="router.push('/library')">
          <el-icon class="menu-item__icon"><Collection /></el-icon>
          <span class="menu-item__text">我的书房</span>
          <el-icon class="menu-item__arrow"><ArrowRight /></el-icon>
        </div>
        <div class="menu-item" @click="router.push('/upload')">
          <el-icon class="menu-item__icon"><Upload /></el-icon>
          <span class="menu-item__text">上传小说</span>
          <el-icon class="menu-item__arrow"><ArrowRight /></el-icon>
        </div>
      </div>

      <div class="menu-group">
        <div class="menu-group__title">账号设置</div>
        <div class="menu-item" @click="handleChangePassword">
          <el-icon class="menu-item__icon"><Lock /></el-icon>
          <span class="menu-item__text">修改密码</span>
          <el-icon class="menu-item__arrow"><ArrowRight /></el-icon>
        </div>
        <div class="menu-item" @click="handleLogout">
          <el-icon class="menu-item__icon" style="color: var(--el-color-danger)"><SwitchButton /></el-icon>
          <span class="menu-item__text" style="color: var(--el-color-danger)">退出登录</span>
          <el-icon class="menu-item__arrow"><ArrowRight /></el-icon>
        </div>
      </div>
    </div>

    <!-- 版本信息 -->
    <div class="user-page__footer">
      <span>小说阅读平台 v1.0.0</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { ElMessage } from 'element-plus';
import { ArrowLeft, ArrowRight, Calendar, Collection, Upload, Lock, SwitchButton } from '@element-plus/icons-vue';
import { useUserStore } from '../stores/user';
import { authApi } from '../services/auth';
import type { UserStats, UserRole, ApiResponse } from '../types/user';
import { ROLE_LABELS } from '../types/user';

const router = useRouter();
const userStore = useUserStore();
const { user } = storeToRefs(userStore);

// ── 头像 ──
const userAvatar = computed(() => '');
const avatarText = computed(() => {
  const name = user.value?.username || '读';
  return name.charAt(0).toUpperCase();
});
const avatarColor = computed(() => user.value?.avatar || '#F5A623');

// ── 角色 ──
const roleLabel = computed(() => {
  const role = (user.value?.role || 'member') as UserRole;
  return ROLE_LABELS[role] || '普通成员';
});

const roleTagType = computed(() => {
  const role = user.value?.role as UserRole;
  if (role === 'admin') return 'danger';
  if (role === 'seed_member') return 'warning';
  return 'info';
});

// ── 统计数据 ──
const stats = ref<UserStats>({
  novel_count: 0,
  bookshelf_count: 0,
  category_count: 0,
  total_size: 0,
});

// ── 格式化 ──
function formatDate(dateStr?: string): string {
  if (!dateStr) return '未知';
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function formatSize(bytes: number): string {
  if (bytes === 0) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
}

// ── 操作 ──
function handleChangePassword() {
  ElMessage.info('修改密码功能开发中');
}

async function handleLogout() {
  const confirmed = await userStore.logout();
  if (confirmed) {
    router.push('/');
  }
}

// ── 初始化 ──
onMounted(async () => {
  try {
    const response = await authApi.getUserStats();
    const res = response as unknown as ApiResponse<UserStats>;
    if (res.code === 0 && res.data) {
      stats.value = res.data;
    }
  } catch {
    // 获取用户统计失败，静默处理
  }
});
</script>

<style scoped lang="scss">
.user-page {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);

  // ── 顶部栏 ──
  &__header {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    background: #fff;
    border-bottom: 1px solid var(--el-border-color-light);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  &__header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__back {
    display: flex;
    align-items: center;
    color: var(--el-text-color-primary);
    text-decoration: none;
    font-size: 20px;
    cursor: pointer;

    &:hover {
      color: var(--el-color-primary);
    }
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
  }

  // ── 用户信息卡片 ──
  &__profile {
    background: linear-gradient(135deg, var(--el-color-primary) 0%, var(--el-color-primary-light-3) 100%);
    padding: 32px 24px 24px;
    color: #fff;
  }

  &__avatar-section {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 16px;
  }

  &__avatar {
    color: #fff;
    font-size: 32px;
    font-weight: 700;
    flex-shrink: 0;
  }

  &__user-info {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  &__username {
    font-size: 22px;
    font-weight: 600;
    margin: 0;
  }

  &__role-tag {
    width: fit-content;
  }

  &__join-date {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    opacity: 0.85;
  }

  // ── 数据统计 ──
  &__stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding: 20px;
    margin-top: -12px;
  }

  // ── 功能菜单 ──
  &__menu {
    padding: 0 20px;
  }

  // ── 底部 ──
  &__footer {
    text-align: center;
    padding: 32px 20px;
    font-size: 12px;
    color: var(--el-text-color-placeholder);
  }
}

// ── 统计卡片 ──
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px 12px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }

  &__value {
    font-size: 24px;
    font-weight: 700;
    color: var(--el-color-primary);
    margin-bottom: 4px;
  }

  &__label {
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}

// ── 菜单组 ──
.menu-group {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;

  &__title {
    padding: 12px 16px 4px;
    font-size: 13px;
    color: var(--el-text-color-secondary);
    font-weight: 500;
  }
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid var(--el-border-color-lighter);

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: var(--el-fill-color-light);
  }

  &__icon {
    font-size: 18px;
    color: var(--el-text-color-primary);
  }

  &__text {
    flex: 1;
    font-size: 15px;
    color: var(--el-text-color-primary);
  }

  &__arrow {
    font-size: 14px;
    color: var(--el-text-color-placeholder);
  }
}
</style>

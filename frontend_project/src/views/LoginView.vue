<template>
  <div class="auth-page">
    <!-- 左侧品牌区 -->
    <div class="auth-page__brand">
      <div class="auth-page__brand-content">
        <div class="auth-page__logo">
          <span class="auth-page__logo-icon">📖</span>
          <h1 class="auth-page__logo-text">小说阅读平台</h1>
        </div>
        <p class="auth-page__slogan">发现好书，沉浸阅读</p>
        <div class="auth-page__illustration">
          <div class="auth-page__book auth-page__book--1">📕</div>
          <div class="auth-page__book auth-page__book--2">📗</div>
          <div class="auth-page__book auth-page__book--3">📘</div>
          <div class="auth-page__book auth-page__book--4">📙</div>
        </div>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="auth-page__form-area">
      <div class="auth-card">
        <h2 class="auth-card__title">欢迎回来 👋</h2>
        <p class="auth-card__subtitle">登录你的账号，继续阅读之旅</p>

        <el-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          label-position="top"
          @keyup.enter="handleLogin"
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="formData.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
              size="large"
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="formData.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
              size="large"
            />
          </el-form-item>

          <div class="auth-card__options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          </div>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="userStore.loading"
              class="auth-card__submit"
              @click="handleLogin"
            >
              登 录
            </el-button>
          </el-form-item>
        </el-form>

        <p class="auth-card__switch">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '../stores/user';
import type { FormInstance, FormRules } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const formRef = ref<FormInstance>();

const formData = reactive({
  username: '',
  password: '',
});

const rememberMe = ref(false);

const formRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
};

async function handleLogin() {
  if (!formRef.value) return;

  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  const success = await userStore.login(formData.username, formData.password);
  if (success) {
    const redirect = (route.query.redirect as string) || '/';
    router.push(redirect);
  }
}
</script>

<style scoped lang="scss">
.auth-page {
  display: flex;
  min-height: 100vh;

  // ── 左侧品牌区 ──
  &__brand {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 30%, #a5d6a7 70%, #81c784 100%);
    position: relative;
    overflow: hidden;

    &::before {
      content: '';
      position: absolute;
      top: -50%;
      right: -30%;
      width: 600px;
      height: 600px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 50%;
    }

    &::after {
      content: '';
      position: absolute;
      bottom: -30%;
      left: -20%;
      width: 400px;
      height: 400px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 50%;
    }
  }

  &__brand-content {
    text-align: center;
    position: relative;
    z-index: 1;
  }

  &__logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 16px;
  }

  &__logo-icon {
    font-size: 48px;
  }

  &__logo-text {
    font-size: 32px;
    font-weight: 700;
    color: #2e7d32;
    margin: 0;
  }

  &__slogan {
    font-size: 18px;
    color: #43a047;
    margin: 0 0 48px;
    letter-spacing: 2px;
  }

  &__illustration {
    display: flex;
    justify-content: center;
    gap: 20px;
  }

  &__book {
    font-size: 48px;
    animation: float 3s ease-in-out infinite;

    &--1 { animation-delay: 0s; }
    &--2 { animation-delay: 0.5s; }
    &--3 { animation-delay: 1s; }
    &--4 { animation-delay: 1.5s; }
  }

  // ── 右侧表单区 ──
  &__form-area {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fafafa;
    padding: 40px;
  }
}

// ── 表单卡片 ──
.auth-card {
  width: 100%;
  max-width: 400px;

  &__title {
    font-size: 28px;
    font-weight: 700;
    color: #2e7d32;
    margin: 0 0 8px;
  }

  &__subtitle {
    font-size: 15px;
    color: #81c784;
    margin: 0 0 32px;
  }

  &__options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  &__submit {
    width: 100%;
    height: 48px;
    font-size: 16px;
    border-radius: 12px;
    background: linear-gradient(135deg, #66bb6a, #43a047);
    border: none;

    &:hover {
      background: linear-gradient(135deg, #81c784, #66bb6a);
    }
  }

  &__switch {
    text-align: center;
    margin: 24px 0 0;
    font-size: 14px;
    color: #9e9e9e;

    a {
      color: #43a047;
      text-decoration: none;
      font-weight: 600;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}

// ── 漂浮动画 ──
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

// ── Element Plus 样式覆盖 ──
:deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 0 0 1px #e0e0e0 inset;

  &:hover {
    box-shadow: 0 0 0 1px #a5d6a7 inset;
  }

  &.is-focus {
    box-shadow: 0 0 0 1px #66bb6a inset;
  }
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #616161;
}
</style>

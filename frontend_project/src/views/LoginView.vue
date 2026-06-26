<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1 class="auth-card__title">登录</h1>

      <el-form ref="formRef" :model="formData" :rules="formRules" label-position="top" @keyup.enter="handleLogin">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" :prefix-icon="User" size="large" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" :prefix-icon="Lock" show-password size="large" />
        </el-form-item>

        <el-form-item>
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" :loading="userStore.loading" class="auth-card__submit" @click="handleLogin">
            登 录
          </el-button>
        </el-form-item>
      </el-form>

      <p class="auth-card__switch">
        没有账号？
        <router-link to="/register">立即注册</router-link>
      </p>
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
    // 登录成功，跳转到 redirect 目标页或首页
    const redirect = (route.query.redirect as string) || '/';
    router.push(redirect);
  }
}
</script>

<style scoped lang="scss">
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--el-color-primary-light-9), var(--el-color-primary-light-7));
}

.auth-card {
  width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);

  &__title {
    text-align: center;
    margin: 0 0 32px;
    font-size: 24px;
    color: var(--el-text-color-primary);
  }

  &__submit {
    width: 100%;
  }

  &__switch {
    text-align: center;
    margin: 16px 0 0;
    font-size: 14px;
    color: var(--el-text-color-secondary);

    a {
      color: var(--el-color-primary);
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
  }
}
</style>

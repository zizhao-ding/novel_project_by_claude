<template>
  <div class="not-found">
    <div class="not-found__content">
      <h1 class="not-found__code">404</h1>
      <p class="not-found__text">页面不存在或已被移除</p>
      <div class="not-found__actions">
        <el-button type="primary" size="large" @click="$router.push('/')">返回首页</el-button>
        <el-button size="large" @click="$router.back()">返回上一页</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped lang="scss">
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);

  &__content {
    text-align: center;
  }

  &__code {
    font-size: 120px;
    font-weight: 700;
    color: var(--el-color-primary-light-3);
    margin: 0 0 16px;
    line-height: 1;
  }

  &__text {
    font-size: 16px;
    color: var(--el-text-color-secondary);
    margin-bottom: 32px;
  }

  &__actions {
    display: flex;
    justify-content: center;
    gap: 12px;
  }
}
</style>

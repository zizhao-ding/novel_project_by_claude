# 08 — 错误处理规范

## 全局错误处理

```typescript
// plugins/error-handler.ts
import type { App } from 'vue';
import { ElMessage } from 'element-plus';

export function setupErrorHandler(app: App) {
  // Vue 全局错误捕获
  app.config.errorHandler = (err, instance, info) => {
    console.error('[Global Error]', err);
    console.error('[Error Info]', info);
    ElMessage.error('系统出现错误，请稍后重试');
  };

  // 未处理的 Promise 拒绝
  window.addEventListener('unhandledrejection', (event) => {
    console.error('[Unhandled Promise]', event.reason);
    ElMessage.error('网络请求失败，请检查网络连接');
    event.preventDefault();
  });
}
```

## 异步操作错误处理

```typescript
// ✅ 标准模式：try-catch-finally
async function fetchData() {
  loading.value = true;
  error.value = null;
  try {
    const data = await api.getData();
    return data;
  } catch (err) {
    error.value = (err as Error).message;
    ElMessage.error(`加载失败：${error.value}`);
    throw err;
  } finally {
    loading.value = false;
  }
}
```

## Store Action 错误处理

```typescript
// ✅ Store action 捕获错误并设置 error state
async function uploadNovel(data: FormData) {
  loading.value = true;
  error.value = null;
  try {
    const novel = await novelApi.upload(data);
    novels.value.unshift(novel);
    ElMessage.success('上传成功');
    return novel;
  } catch (err) {
    const msg = (err as Error).message;
    error.value = msg;
    ElMessage.error(`上传失败：${msg}`);
    throw err;
  } finally {
    loading.value = false;
  }
}
```

## HTTP 错误码处理

| 状态码 | 处理方式 |
|--------|----------|
| 400 | 显示后端返回的错误消息 |
| 401 | 清除登录状态，跳转登录页 |
| 403 | 提示"无权限访问" |
| 404 | 提示"资源不存在" |
| 500+ | 提示"服务器错误，请稍后重试" |
| Network Error | 提示"网络连接失败，请检查网络" |

## ✅ 规则速查

- ✅ 所有 `async` 操作必须有 `try-catch`
- ✅ 捕获错误后必须给用户可见的提示（ElMessage）
- ✅ API 层错误由拦截器统一处理，业务层处理业务错误
- ❌ 禁止吞掉错误不处理（空 `catch` 块）
- ❌ 禁止将原始错误对象直接展示给用户

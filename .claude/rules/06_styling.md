# 06 — 样式 & CSS 规范

## 技术方案

**UnoCSS**（原子化 CSS）+ **SCSS**（自定义样式，BEM 命名）+ **Element Plus CSS 变量**。

## BEM 命名规范

```scss
// Block（块）
.user-card {
  padding: 16px;
  border: 1px solid var(--el-border-color);
  border-radius: 8px;

  // Element（元素）— 使用 __ 连接
  &__header {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }

  &__avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
  }

  &__content {
    flex: 1;
  }

  // Modifier（修饰符）— 使用 -- 连接
  &--featured {
    border-color: var(--el-color-primary);
    box-shadow: 0 0 8px rgba(var(--el-color-primary-rgb), 0.2);
  }

  &--disabled {
    opacity: 0.5;
    pointer-events: none;
  }
}
```

## Element Plus CSS 变量

```scss
// ✅ 使用 Element Plus CSS 变量，保持主题统一
.custom-component {
  color: var(--el-color-primary);
  background: var(--el-bg-color);
  border-color: var(--el-border-color);

  &:hover {
    color: var(--el-color-primary-light-3);
  }
}
```

## SCSS 文件组织

```scss
// styles/variables.scss — 项目级变量
$primary-color: #409eff;
$text-color: #303133;
$border-color: #dcdfe6;
$sidebar-width: 240px;

// styles/mixins.scss — 可复用 Mixin
@mixin text-ellipsis($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

## 样式作用域

```vue
<!-- ✅ 组件样式使用 scoped -->
<style scoped lang="scss">
.component { }
</style>

<!-- ✅ 全局样式放在 src/assets/styles/ 下 -->
<!-- ❌ 避免在组件中写非 scoped 样式 -->
```

## ✅ 推荐 vs ❌ 避免

- ✅ 优先使用 UnoCSS 原子类（`flex`, `p-4`, `text-center`）
- ✅ 复杂样式使用 BEM + SCSS
- ✅ 颜色/间距使用 Element Plus CSS 变量
- ❌ 禁止内联样式（`style="color: red"`）
- ❌ 禁止使用 `!important`（除非覆盖第三方库样式）
- ❌ 禁止使用 ID 选择器（`#app` 除外）

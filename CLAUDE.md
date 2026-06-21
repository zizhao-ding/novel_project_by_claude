# CLAUDE.md

> 本项目的前端开发规范入口。AI 在生成、审查、修改任何前端代码时，必须遵循本文件及关联的规则体系。

## 项目概述

这是一个**小说在线阅读平台**，支持图片和文本小说（TXT格式）的上传及在线阅读，专注于 PC 端网页体验。

## 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 (Composition API + `<script setup>`) | ^3.5 |
| 语言 | **TypeScript**（强制，禁止纯 JS） | - |
| 构建 | Vite | ^8.0 |
| UI 库 | **Element Plus**（按需导入） | - |
| CSS 方案 | UnoCSS + SCSS (BEM 命名) | - |
| 状态管理 | Pinia (Setup Store 模式) | ^3.0 |
| 路由 | Vue Router (懒加载) | ^4.6 |
| HTTP | Axios (统一拦截器封装) | ^1.18 |
| 国际化 | vue-i18n | ^11.4 |
| 工具库 | @vueuse/core | ^14.3 |

## Rules & Spec 体系

```
CLAUDE.md                          ← 你在这里（主入口）
├── .claude/rules/                 ← 📋 规则：定义 HOW（怎么写代码）
│   ├── 01_project_structure.md    ← 目录结构 & 文件命名
│   ├── 02_vue3_components.md      ← Vue 3 组件开发规范
│   ├── 03_typescript.md           ← TypeScript 类型规范
│   ├── 04_state_management.md     ← Pinia 状态管理
│   ├── 05_api_services.md         ← API 服务层
│   ├── 06_styling.md              ← 样式 & CSS 规范
│   ├── 07_routing.md              ← 路由规范
│   ├── 08_error_handling.md       ← 错误处理
│   ├── 09_git_conventions.md      ← Git 提交规范
│   └── 10_progress_tracking.md    ← 进度自动记录
└── spec/                          ← 📐 规格：定义 WHAT（要做什么）
    ├── _template.md               ← 功能规格模板
    └── 01_auth_register.md        ← 示例：用户认证规格
```

- **规则（Rule）**：持久有效的编码标准，每次写代码时自动适用。
- **规格（Spec）**：按功能定义的需求文档，实现某个功能前必须先阅读对应 spec。

完整的规范参考手册见：`前端开发规范.md`（760行完整版，rules 文件是其精华提取）。

## AI 开发工作流

当接到前端开发任务时，按以下流程执行：

1. **读取 Spec** → 在 `spec/` 目录查找对应功能规格，理解需求和验收标准
2. **加载 Rules** → 根据任务类型加载相关规则文件（至少加载 `01_project_structure.md` 和 `02_vue3_components.md`）
3. **遵循规范** → 生成代码时严格遵循 rules 中的 ✅ 示例，避免 ❌ 示例
4. **验证一致性** → 确保代码风格与已有代码保持一致

## 关键约束速查

以下规则**不可违反**：

- ✅ **必须使用 TypeScript**，所有 `.vue` 文件使用 `<script setup lang="ts">`
- ✅ **必须使用 Element Plus** 作为 UI 组件库，禁止引入其他 UI 库
- ✅ **必须使用 Composition API**（`ref`, `computed`, `watch` 等），禁止 Options API
- ✅ **必须使用 Pinia Setup Store** 模式（`defineStore('name', () => { ... })`）
- ✅ **必须使用 BEM 命名** 编写自定义样式
- ✅ 路由组件**必须懒加载**（`() => import(...)`）
- ✅ 所有异步操作**必须有错误处理**
- ❌ 禁止使用 `var`、`==`（使用 `const`/`let`、`===`）
- ❌ 禁止在模板中使用复杂表达式（抽取为 `computed`）
- ❌ 禁止直接操作 DOM（使用 Vue 响应式绑定）

## 后端协作

后端项目在 `backend_project/`，基于 Python FastAPI + SQLite。
前端通过 `/api` 前缀调用后端接口，开发时 Vite 代理到 `http://localhost:8000`。

API 规范详见：`技术选型.md`

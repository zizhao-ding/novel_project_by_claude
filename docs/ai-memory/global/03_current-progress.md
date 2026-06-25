# 当前开发进度

> **类型**: 项目进度
> **最后更新**: 2026-06-25

## 已完成

### 基础设施

- [x] 前端项目脚手架（Vue 3 + Vite + Element Plus + Pinia + Vue Router）
- [x] 后端项目搭建（FastAPI + SQLite + SQLModel）
- [x] Harness 六层架构整合
- [x] 前端：main.js → main.ts 迁移 + App.vue 改造为 router-view
- [x] 前端：Vite 代理配置 + @ 别名 + SCSS 支持
- [x] Commitlint + Husky — git commit 自动校验格式
- [x] Claude Code PreCommit Hook — 提交前自动 Prettier 格式化
- [x] GitHub PR 模板（`.github/PULL_REQUEST_TEMPLATE.md`）

### 用户认证模块 (REQ-001) ✅

- [x] 前端：用户类型定义（`types/user.ts`）
- [x] 前端：API 服务层（`services/api.ts` + `services/auth.ts`）
- [x] 前端：userStore（`stores/user.ts`）— Pinia Setup Store，含 token 持久化
- [x] 前端：路由守卫（`router/guards.ts` + 更新 `router/index.ts`）
- [x] 前端：登录页（`LoginView.vue`）— 含表单校验、loading 状态
- [x] 前端：注册页（`RegisterView.vue`）— 含密码确认校验
- [x] 前端：首页（`HomeView.vue`）— 含登录/登出状态展示
- [x] 后端：用户注册 API（`POST /api/auth/register`）
- [x] 后端：用户登录 API（`POST /api/auth/login`）— 含 JWT Token 签发
- [x] 后端：用户信息 API（`GET /api/auth/profile`）— 含 Token 验证
- [x] 后端：密码 bcrypt 哈希存储

### 小说上传模块 (REQ-P1-002) ✅

- [x] 前端：小说上传功能（UploadView + useNovelStore + novel API）
- [x] 后端：小说上传/列表/删除 API（`api/novel.py`）
- [x] 后端：Novel 模型 + Schema
- [x] 存储方案：本地文件系统 `uploads/novels/`
- [x] 敏感操作二次确认（删除小说）

## 待开始

#### Phase 2 - 功能扩展
- [ ] 前端：书房页（LibraryView.vue）— 当前为占位页面 (REQ-P2-001)
- [ ] 前端：阅读器（ReaderView.vue）— 当前为占位页面 (REQ-P2-002)

#### Phase 3 - 功能完善
- [ ] 前端：国际化配置（vue-i18n）(REQ-P3-001)

#### 工具链
- [ ] 工具链：ESLint + Prettier + tsconfig.json

## 技术笔记

- **Vite 8 + Rolldown**: `resolve.alias` 构建不生效，当前使用相对路径导入。已保留 alias 配置供 dev server 使用
- **Element Plus**: `ElMessage` 等通过 `unplugin-auto-import` 自动注入，`.ts` 文件中无需显式导入
- **SCSS**: 使用 `sass`（非 `sass-embedded`，因 macOS 12 兼容性）

## 当前分支

`feature_zizhao`

**Why:** 每次新对话时快速了解开发进展，无缝接续工作。

**How to apply:** 每完成一个功能后，更新本文件的 checkbox 状态。

**相关记忆**: [[01_project-overview]] [[04_harness-architecture]]

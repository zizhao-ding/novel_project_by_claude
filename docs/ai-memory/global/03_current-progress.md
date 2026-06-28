# 当前开发进度

> **类型**: 项目进度
> **最后更新**: 2026-06-28

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
- [x] ESLint + TypeScript 严格模式 + Prettier 工具链（`a520156`）
- [x] tsconfig.json + eslint.config.js + TOOLING.md

### 用户认证模块 (REQ-P1-001) ✅

- [x] 前端：用户类型定义（`types/user.ts`）
- [x] 前端：API 服务层（`services/api.ts` + `services/auth.ts`）
- [x] 前端：userStore（`stores/user.ts`）— Pinia Setup Store，含 token 持久化
- [x] 前端：路由守卫（`router/guards.ts` + 更新 `router/index.ts`）
- [x] 前端：登录页（`LoginView.vue`）— 两栏清新风格 + 绿色渐变 + 漂浮书本
- [x] 前端：注册页（`RegisterView.vue`）— 两栏风格 + 头像选择器 8 色
- [x] 后端：用户注册 API（`POST /api/auth/register`）
- [x] 后端：用户登录 API（`POST /api/auth/login`）— 含 JWT Token 签发
- [x] 后端：用户信息 API（`GET /api/auth/profile`）— 含 Token 验证
- [x] 后端：密码 bcrypt 哈希存储
- [x] 修改密码功能（`POST /api/auth/change-password`）— 旧密码校验 + 新密码更新

### 小说上传模块 (REQ-P1-002) ✅

- [x] 前端：小说上传功能（UploadView + useNovelStore + novel API）
- [x] 后端：小说上传/列表/删除 API（`api/novel.py`）
- [x] 后端：Novel 模型 + Schema
- [x] 存储方案：本地文件系统 `uploads/novels/`
- [x] 敏感操作二次确认（删除小说含书名）
- [x] 上传后一键加入书架

### 书房页面 (REQ-P2-001) ✅

- [x] 前端：长按检测 composable `useLongPress.ts`
- [x] 前端：书房页 `LibraryView.vue`（书架网格 + 多选 + 分类 + 删除）
- [x] 前端：统一 AppHeader 顶栏
- [x] 右侧分类栏（10% 宽度，支持新建分类，不同颜色区分）
- [x] 长按/右键进入多选模式
- [x] 批量删除（二次确认，从书架移除）
- [x] 批量分类（弹窗选择，支持弹窗内新建）
- [x] 后端：Category 模型 + CRUD API
- [x] 后端：Bookshelf 模型 + 书架 API
- [x] 后端：Novel 模型新增 category_id
- [x] 后端：批量修改分类 API
- [x] 前端：Category Store + API 服务
- [x] 前端：Bookshelf Store + API 服务
- [x] 种子数据脚本（test 用户 + 6 本假数据）

### 阅读器 (REQ-P2-002) ✅

- [x] 前端：ReaderView.vue 重写（侧边栏目录 + 正文区 + 底部工具栏）
- [x] 三种阅读主题（日间/夜间/护眼）
- [x] 字号调节 12-24px
- [x] 章节导航（上一章/下一章/章节列表侧边栏）
- [x] 阅读进度自动保存，重新进入提示恢复
- [x] 前端：services/reader.ts + stores/reader.ts
- [x] 后端：ReadingProgress 模型 + 进度 API
- [x] 后端：章节列表 + 内容获取 API

### 用户页面 (REQ-P2-003) ✅

- [x] 前端：UserView.vue（头像 + 用户名 + 角色标签 + 统计 + 菜单）
- [x] 后端：User 模型新增 role 字段（admin / seed_member / member）
- [x] 后端：用户统计接口 `/api/auth/user/stats`
- [x] 后端：profile 接口返回 role + avatar
- [x] 前端：User 类型增加 role + avatar + 统计类型
- [x] 前端：auth API 增加 getUserStats / changePassword
- [x] 修改密码弹窗（旧密码校验 + 新密码确认）

### 首页发现页 + 搜索 (REQ-P3-002) ✅

- [x] 前端：HomeView.vue 重写为内容发现页（热门推荐 + 最新上传 + 分类浏览）
- [x] 前端：SearchView.vue 搜索结果页
- [x] 前端：NovelCard.vue 通用小说卡片组件
- [x] 后端：热门推荐/最新上传/搜索 API（3 个端点）
- [x] 前端：services/home.ts + services/search.ts + stores/home.ts
- [x] 搜索和首页对未登录用户开放

### 全局顶栏 AppHeader ✅

- [x] 前端：AppHeader.vue 全局顶栏组件
- [x] 返回按钮区域（箭头 + 标题整块可点击，扩大点击区域）
- [x] 搜索入口
- [x] 头像悬浮卡片（头像/用户名/角色/快捷入口）
- [x] 管理员悬浮卡片显示用户管理入口
- [x] 统一替换 Library/Upload/User/Login/Register 等页面顶栏

### 权限系统 (REQ-P3-004) ✅

- [x] 三级角色体系（admin / seed_member / member）
- [x] 小说可见性标签（public / seed / admin）
- [x] 前端：composables/usePermission.ts 权限判断
- [x] 前端：AdminUsersView.vue 用户角色管理页
- [x] 前端：路由 role 守卫（`meta.roles`）
- [x] 后端：require_role / require_min_role 权限依赖函数
- [x] 后端：admin.py 用户管理接口（列表/角色修改/搜索）
- [x] 后端：小说下载接口 + 可见性过滤
- [x] 设计决策：移除书架阅读限制，纯可见性控制（书架回归收藏夹本质）

### 帮助页 (REQ-P3-003) ✅

- [x] 前端：HelpView.vue FAQ 折叠面板帮助页
- [x] 前端：路由 `/help` + 404 catch-all（NotFoundView.vue）

## 进行中

_当前无进行中的需求_

## 待开始

#### Phase 3 - 功能完善
- [ ] 前端：国际化配置 vue-i18n (REQ-P3-001)

## 已知技术债务

- [ ] **测试覆盖率仍不足** — 前端 2 文件 13 用例（~15%），后端 3 文件 23 用例（~35%），详见 [[05_testing-debt]]
- [x] Layer 2 规范层已补全 — `detail/` 3 文件 + `module/` 3 文件
- [x] Layer 3 方案层已建立 — 5 条 ADR，详见 [[06_architecture-decisions]]
- [x] Layer 5 审核层已建立 — `code-review.md` 审核清单 + 质量标准
- [ ] `docs/specs/detail/` 和 `docs/specs/module/` 目录已填充

## 技术笔记

- **Vite 8 + Rolldown**: `resolve.alias` 构建不生效，当前使用相对路径导入。已保留 alias 配置供 dev server 使用
- **Element Plus**: `ElMessage` 等通过 `unplugin-auto-import` 自动注入，`.ts` 文件中无需显式导入
- **SCSS**: 使用 `sass`（非 `sass-embedded`，因 macOS 12 兼容性）
- **ESLint**: 使用扁平配置 `eslint.config.js`（ESLint v9 格式）

## 当前分支

`feature_zizhao`

**Why:** 每次新对话时快速了解开发进展，无缝接续工作。

**How to apply:** 每完成一个功能后，更新本文件的 checkbox 状态。新会话启动时读取本文件了解当前进度。

**相关记忆**: [[01_project-overview]] [[04_harness-architecture]] [[05_testing-debt]] [[06_architecture-decisions]]

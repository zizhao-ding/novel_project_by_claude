# 📚 小说阅读平台 - 项目总索引

> **最后更新**: 2026-06-28
> **项目阶段**: 开发中

## 项目概述

这是一个**小说在线阅读平台**，支持图片和文本小说（TXT格式）的上传及在线阅读，专注于 PC 端网页体验。

采用 **Harness 六层架构**实现 AI 驱动开发。

## 文档导航

### 📋 需求文档
- **路径**: `docs/requirements/`
- **索引**: [需求索引](requirements/index.md)
- **说明**: 功能需求、验收标准、状态管理

### 📐 规范文档
| 类型 | 路径 | 读取时机 | 说明 |
|------|------|----------|------|
| 核心规范 | `docs/specs/core/` | 启动时必读 | 编码规范、架构规范、Hook 规则、进度跟踪 |
| 详细规范 | `docs/specs/detail/` | 按需读取 | 详细实现指南 |
| 模块规范 | `docs/specs/module/` | 开发特定模块时 | 模块特定规范 |

### 🧠 记忆文档
- **全局经验**: `docs/ai-memory/global/` - 跨模块的经验积累
- **模块经验**: `docs/ai-memory/module/` - 特定模块的经验

## 快速开始

### 新会话启动流程

当开始新的开发会话时，**必须**按顺序执行：

1. **读取本文件**: `docs/index.md` - 了解项目整体结构
2. **读取需求索引**: `docs/requirements/index.md` - 了解当前需求状态
3. **读取核心规范**: `docs/specs/core/` - 编码规范、架构规范、Hook 规则

### 常用命令

```bash
# 启动前端开发服务器
cd frontend_project && npm run dev

# 启动后端服务
cd backend_project && python -m uvicorn app.main:app --reload

# 构建前端
cd frontend_project && npm run build
```

## 项目结构

```
novel_project_by_claude/
├── frontend_project/       # 前端项目 (Vue 3 + Element Plus)
├── backend_project/        # 后端项目 (Python FastAPI + SQLite)
├── docs/                   # 📚 项目文档 (Harness 架构)
│   ├── index.md            # 本文件 - 总索引
│   ├── requirements/       # 需求文档
│   ├── specs/              # 规范文档
│   │   ├── core/           # 核心规范 (启动时必读)
│   │   ├── detail/         # 详细规范
│   │   └── module/         # 模块规范
│   └── ai-memory/          # AI 记忆文档
│       ├── global/         # 全局经验
│       └── module/         # 模块经验
└── .claude/                # Claude Code 配置
    └── settings.local.json # 权限和 hooks 配置
```

## Harness 六层架构

```
┌─────────────────────────────────────────────┐
│  Layer 6: 验收层 (Acceptance)                │
│  - 自动化测试                                │
│  - 验收标准检查                              │
│  - 状态更新                                  │
├─────────────────────────────────────────────┤
│  Layer 5: 审核层 (Review)                    │
│  - 代码审核                                  │
│  - 规范检查                                  │
│  - 质量评估                                  │
├─────────────────────────────────────────────┤
│  Layer 4: 执行层 (Execution)                 │
│  - 代码生成                                  │
│  - 文件操作                                  │
│  - 构建部署                                  │
├─────────────────────────────────────────────┤
│  Layer 3: 方案层 (Solution)                  │
│  - 技术方案                                  │
│  - 架构设计                                  │
│  - 接口定义                                  │
├─────────────────────────────────────────────┤
│  Layer 2: 规范层 (Specification)             │
│  - 编码规范                                  │
│  - 架构规范                                  │
│  - Hook 规则                                 │
├─────────────────────────────────────────────┤
│  Layer 1: 需求层 (Requirement)               │
│  - 需求文档                                  │
│  - 验收标准                                  │
│  - 状态管理                                  │
└─────────────────────────────────────────────┘
```

## 当前状态

### 项目阶段
- **当前阶段**: 开发中
- **已完成需求**: 8 个
- **进行中**: 0 个
- **待处理**: 2 个

### 需求列表

| 需求编号 | 需求名称 | 状态 | 优先级 |
|----------|----------|------|--------|
| REQ-P1-001 | 用户注册与登录 | ✅ done | P0 |
| REQ-P1-002 | 小说上传与管理 | ✅ done | P0 |
| REQ-P2-001 | 书房页面 | ✅ done | P1 |
| REQ-P2-002 | 阅读器 | ✅ done | P1 |
| REQ-P2-003 | 用户页面 | ✅ done | P1 |
| REQ-P3-001 | 国际化支持 | 📝 pending | P2 |
| REQ-P3-002 | 首页发现页 + 搜索 | ✅ done | P1 |
| REQ-P3-003 | 使用帮助页 | ✅ done | P2 |
| REQ-P3-004 | 权限系统 | ✅ done | P0 |
| REQ-P3-005 | 小说详情页 | 📝 pending | P1 |

### 已完成

#### 基础设施
- [x] Rules & Spec 体系建立
- [x] Harness 六层架构整合
- [x] 前端项目脚手架（Vue 3 + Vite + Element Plus + Pinia + Vue Router）
- [x] 后端项目搭建（FastAPI + SQLite + SQLModel）
- [x] 前端：main.js → main.ts 迁移 + App.vue 改造
- [x] 前端：Vite 代理配置 + @ 别名 + SCSS 支持
- [x] Commitlint + Husky — git commit 自动校验格式
- [x] Claude Code PreCommit Hook — 提交前自动 Prettier 格式化
- [x] GitHub PR 模板

#### 用户认证模块 (REQ-P1-001) ✅ done
- [x] 用户类型定义 `types/user.ts`（含 role、avatar、AVATAR_PRESETS）
- [x] API 服务层 `services/api.ts` + `services/auth.ts`
- [x] 用户 Store `stores/user.ts`（Pinia Setup Store + token 持久化）
- [x] 路由守卫 `router/guards.ts` + 路由更新
- [x] 登录页 `LoginView.vue`（两栏清新风格 + 绿色渐变 + 漂浮书本）
- [x] 注册页 `RegisterView.vue`（两栏风格 + 头像选择器 8 色）
- [x] 首页 `HomeView.vue`（登录/登出状态展示）
- [x] 后端认证接口：register、login、profile（含 JWT + avatar）
- [x] 后端 CORS + 配置模块
- [x] 密码加密：bcrypt 哈希存储

#### 小说上传模块 (REQ-P1-002) ✅ done（已重构）
- [x] 小说类型定义 `types/novel.ts`
- [x] 小说 API 服务 `services/novel.ts`
- [x] 小说 Store `stores/novel.ts`（职责分离：确认弹窗在视图层）
- [x] 上传页 `UploadView.vue`（统一顶部栏 + 卡片网格 + 加入书架）
- [x] 后端小说 API：upload、list、delete
- [x] 后端 Novel 模型 + Schema
- [x] 存储方案：本地文件系统 `uploads/novels/`
- [x] 敏感操作二次确认（删除小说含书名）
- [x] 上传后一键加入书架

#### 书房页面 (REQ-P2-001) ✅ done
- [x] 长按检测 composable `composables/useLongPress.ts`
- [x] 书房页 `LibraryView.vue`（书架网格 + 多选 + 分类 + 删除）
- [x] 顶部栏：返回按钮 + 标题 + 用户头像
- [x] 右侧分类栏（10% 宽度，支持新建分类，不同颜色区分）
- [x] 分类筛选（点击分类筛选书籍）
- [x] 长按/右键进入多选模式
- [x] 批量删除（二次确认，从书架移除）
- [x] 批量分类（弹窗选择，支持弹窗内新建）
- [x] 后端：Category 模型 + CRUD API
- [x] 后端：Bookshelf 模型 + 书架 API
- [x] 后端：Novel 模型新增 category_id
- [x] 后端：批量修改分类 API（修复路由冲突）
- [x] 前端：Category Store + API 服务
- [x] 前端：Bookshelf Store + API 服务
- [x] 种子数据脚本（test 用户 + 6 本假数据）

#### 用户页面 (REQ-P2-003) ✅ done
- [x] 用户页面 `UserView.vue`（头像 + 用户名 + 角色 + 统计 + 菜单）
- [x] 后端：User 模型新增 role 字段（admin / seed_member / member）
- [x] 后端：用户统计接口 `/api/auth/user/stats`
- [x] 后端：profile 接口返回 role
- [x] 前端：User 类型增加 role + 统计类型
- [x] 前端：auth API 增加 getUserStats
- [x] 书房页头像点击跳转用户页

#### 阅读器 (REQ-P2-002) ✅ done
- [x] ReaderView.vue（侧边栏目录 + 正文区 + 底部工具栏）
- [x] 三种阅读主题 + 字号调节 12-24px
- [x] 阅读进度自动保存恢复
- [x] services/reader.ts + stores/reader.ts
- [x] 后端 ReadingProgress 模型

#### 首页发现页 + 搜索 (REQ-P3-002) ✅ done
- [x] 首页重写为内容发现页 + SearchView 搜索
- [x] NovelCard 通用小说卡片 + AppHeader 全局顶栏
- [x] 后端热门/最新/搜索 API

#### 权限系统 (REQ-P3-004) ✅ done
- [x] 三级角色 + 三级可见性
- [x] usePermission composable + AdminUsersView 管理页
- [x] 路由 role 守卫 + 后端权限依赖注入

#### 帮助页 + 修改密码 (REQ-P3-003) ✅ done
- [x] HelpView + NotFoundView + 修改密码弹窗

#### 工具链 ✅
- [x] ESLint v9 + TypeScript 严格模式 + Prettier

### 待开始

#### Phase 3 - 功能完善
- [ ] 前端：国际化配置 vue-i18n (REQ-P3-001)
- [ ] 小说详情页 (REQ-P3-005)

---

*本文件由 AI 维护，请勿手动编辑关键部分*

# 📚 小说阅读平台 - 项目总索引

> **最后更新**: 2026-06-25
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
cd front_project && npm run dev

# 启动后端服务
cd backend_project && python -m uvicorn app.main:app --reload

# 构建前端
cd front_project && npm run build
```

## 项目结构

```
novel_project_by_claude/
├── front_project/          # 前端项目 (Vue 3 + Element Plus)
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
- **已完成需求**: 2 个
- **进行中**: 0 个
- **待处理**: 0 个

### 需求列表

| 需求编号 | 需求名称 | 状态 | 优先级 |
|----------|----------|------|--------|
| REQ-P1-001 | 用户注册与登录 | ✅ done | P0 |
| REQ-P1-002 | 小说上传与管理 | ✅ done | P0 |

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

#### 用户认证模块 (REQ-P1-001)
- [x] 用户类型定义 `types/user.ts`
- [x] API 服务层 `services/api.ts` + `services/auth.ts`
- [x] 用户 Store `stores/user.ts`（Pinia Setup Store + token 持久化）
- [x] 路由守卫 `router/guards.ts` + 路由更新
- [x] 登录页 `LoginView.vue`（表单校验 + loading 状态）
- [x] 注册页 `RegisterView.vue`（密码确认校验）
- [x] 首页 `HomeView.vue`（登录/登出状态展示）
- [x] 后端认证接口：register、login、profile（含 JWT）
- [x] 后端 CORS + 配置模块
- [x] 密码加密：bcrypt 哈希存储

#### 小说上传模块 (REQ-P1-002)
- [x] 小说类型定义 `types/novel.ts`
- [x] 小说 API 服务 `services/novel.ts`
- [x] 小说 Store `stores/novel.ts`
- [x] 上传页 `UploadView.vue`（拖拽上传 + 进度条）
- [x] 后端小说 API：upload、list、delete
- [x] 后端 Novel 模型 + Schema
- [x] 存储方案：本地文件系统 `uploads/novels/`
- [x] 敏感操作二次确认（删除小说）

### 待开始

#### Phase 2 - 功能扩展
- [ ] 前端：书房页（LibraryView.vue）— 当前为占位页面 (REQ-P2-001)
- [ ] 前端：阅读器（ReaderView.vue）— 当前为占位页面 (REQ-P2-002)

#### Phase 3 - 功能完善
- [ ] 前端：国际化配置（vue-i18n）(REQ-P3-001)

#### 工具链
- [ ] 工具链：ESLint + Prettier + tsconfig.json

---

*本文件由 AI 维护，请勿手动编辑关键部分*

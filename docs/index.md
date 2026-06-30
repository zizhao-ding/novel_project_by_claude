# 📚 小说阅读平台 — 项目总索引

> **最后更新**: 2026-06-30
> **项目阶段**: 开发中

## 项目概述

这是一个**小说在线阅读平台**，支持图片和文本小说（TXT格式）的上传及在线阅读，专注于 PC 端网页体验。

采用 **AI Agent 原生六层架构**实现 AI 驱动开发。架构总纲：`docs/specs/core/ai-agent-architecture.md`

## AI Agent 六层架构

```
┌──────────────────────────────────────────────────────────────────┐
│                      AI Agent 运行时治理                          │
│                                                                   │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   │ 规范层    │  │ 上下文层  │  │ 约束层    │  │ 记忆层    │  │ 工具层    │  │ 工作流层  │
│   │          │  │          │  │          │  │          │  │          │  │          │
│   │ "代码    │  │ "现在    │  │ "绝对    │  │ "过去    │  │ "我能    │  │ "按什么  │
│   │  应该    │  │  在做什么"│  │  不      │  │  学到    │  │  做什么" │  │  步骤做" │
│   │  长什么样"│  │          │  │  能做的" │  │  了什么" │  │          │  │          │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
│        │              │              │              │              │              │
│        ▼              ▼              ▼              ▼              ▼              ▼
│   编码规范        项目概述        TS强制         经验教训       Bash/Write    开发SOP
│   架构规范        需求索引        Element+        架构决策        Agent/MCP     修复SOP
│   样式规范        当前进度        禁止项          技术债务        权限边界      审查SOP
│        │              │              │              │              │              │
│        └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
│                                         │
│                         六层同时生效，持续约束 AI 的每一个行为
└──────────────────────────────────────────────────────────────────┘
```

> 架构说明：这是从旧 Harness 六层架构（需求→规范→方案→执行→审核→验收）演进而来。
> 旧 Harness 的内容已全部融合进新六层。映射关系详见架构总纲第6节。

## 文档导航（按六层组织）

### 📐 规范层 — "代码应该长什么样"

| 文档 | 路径 | 说明 |
|------|------|------|
| 编码规范 | `docs/specs/core/coding-standards.md` | 文件命名、Vue组件、TypeScript、SCSS/BEM、Git |
| 架构规范 | `docs/specs/core/architecture.md` | Pinia Store、API服务、路由、错误处理 |
| 详细规范 | `docs/specs/detail/` | 按需读取的详细实现指南 |
| 模块规范 | `docs/specs/module/` | 特定模块的开发规范 |

### 🔴 约束层 — "什么绝对不能做"

| 文档 | 路径 | 说明 |
|------|------|------|
| 约束层定义 | `docs/specs/core/constraint-layer.md` | 30条硬性红线（C-001 ~ C-030） |
| Hook 规则 | `docs/specs/core/hook-rules.md` | PreToolUse / PostToolUse 检查机制 |

### 📋 上下文层 — "现在在做什么"

| 文档 | 路径 | 说明 |
|------|------|------|
| 需求索引 | `docs/requirements/index.md` | 所有需求的状态追踪 |
| 需求文档 | `docs/requirements/phase*/` | 各阶段需求详细文档 |
| AI 运行时配置 | `CLAUDE.md` | 项目根目录，AI 会话入口 |

### 🧠 记忆层 — "过去学到了什么"

| 文档 | 路径 | 说明 |
|------|------|------|
| 当前进度 | `docs/ai-memory/global/03_current-progress.md` | 已完成/进行中/待开始 |
| 架构决策 | `docs/ai-memory/global/06_architecture-decisions.md` | 5条 ADR 记录 |
| 技术债务 | `docs/ai-memory/global/05_testing-debt.md` | 测试覆盖率改进计划 |
| 模块经验 | `docs/ai-memory/module/` | 特定模块的经验 |

### 🔧 工具层 — "能做什么"

| 配置 | 路径 | 说明 |
|------|------|------|
| Claude Code 设置 | `.claude/settings.local.json` | 权限和 hooks 配置 |

### 🔄 工作流层 — "按什么流程做"

| 流程 | 入口 | 说明 |
|------|------|------|
| 会话启动流程 | `CLAUDE.md` → 工作流层 | 自动执行 |
| 标准开发流程 | `CLAUDE.md` → 工作流层 | 需求→方案→执行→审核→验收 |
| 快速修复流程 | `CLAUDE.md` → 工作流层 | 定位→确认→修改→验证 |
| 代码审查流程 | `CLAUDE.md` → 工作流层 | 加载→对照→输出报告 |
| 会话结束流程 | `CLAUDE.md` → 工作流层 | 更新进度→沉淀记忆 |

## 快速开始

### 新会话启动流程

当开始新的开发会话时，**按顺序加载上下文**：

1. **读取本文件** `docs/index.md` → 了解项目全貌
2. **读取需求索引** `docs/requirements/index.md` → 了解需求状态
3. **读取约束层** `docs/specs/core/constraint-layer.md` → 加载硬性红线
4. **读取当前进度** `docs/ai-memory/global/03_current-progress.md`
5. **读取架构决策** `docs/ai-memory/global/06_architecture-decisions.md`

### 常用命令

```bash
# 启动前端开发服务器
cd frontend_project && npm run dev

# 启动后端服务
cd backend_project && python -m uvicorn app.main:app --reload

# 构建前端
cd frontend_project && npm run build

# 代码检查
cd frontend_project && npm run lint
cd frontend_project && npm run type-check
```

## 项目结构

```
novel_project_by_claude/
├── CLAUDE.md                          # 🎯 AI Agent 运行时入口
├── frontend_project/                  # 前端项目 (Vue 3 + Element Plus)
├── backend_project/                   # 后端项目 (Python FastAPI + SQLite)
├── docs/                              # 📚 项目文档
│   ├── index.md                       #   本文件 — 总索引
│   ├── specs/core/                    #   规范层 + 约束层
│   │   ├── ai-agent-architecture.md   #   架构总纲
│   │   ├── coding-standards.md        #   编码规范
│   │   ├── architecture.md            #   架构规范
│   │   ├── constraint-layer.md        #   约束层定义
│   │   └── hook-rules.md              #   Hook 规则
│   ├── specs/detail/                  #   详细规范
│   ├── specs/module/                  #   模块规范
│   ├── requirements/                  #   需求文档
│   └── ai-memory/                     #   记忆文档
└── .claude/                           # Claude Code 配置
    └── settings.local.json            #   权限和 hooks 配置
```

## 当前状态

### 项目阶段
- **当前阶段**: 开发中
- **已完成需求**: 9 个
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
| REQ-P3-004 | 权限系统（角色+可见性+角色管理） | ✅ done | P0 |
| REQ-P3-005 | 小说详情页 | 📝 pending | P1 |

### 已完成摘要

#### 基础设施
- [x] 前端项目脚手架 + 后端项目搭建
- [x] ESLint v9 + TypeScript 严格模式 + Prettier + Commitlint + Husky
- [x] GitHub PR 模板

#### 用户认证 (REQ-P1-001) ✅
- [x] 登录/注册/个人信息 + JWT + bcrypt + 路由守卫 + 修改密码

#### 小说上传 (REQ-P1-002) ✅
- [x] 上传/列表/删除 + 一键加入书架 + 二次确认

#### 书房 (REQ-P2-001) ✅
- [x] 书架网格 + 分类系统 + 多选/批量操作 + 种子数据

#### 阅读器 (REQ-P2-002) ✅
- [x] 三主题 + 字号调节 + 进度持久化 + 章节导航

#### 用户页 (REQ-P2-003) ✅
- [x] 用户信息 + 角色标签 + 统计数据 + 修改密码弹窗

#### 首页 + 搜索 (REQ-P3-002) ✅
- [x] 内容发现页 + 搜索页 + NovelCard 通用卡片 + AppHeader 全局顶栏

#### 权限系统 (REQ-P3-004) ✅
- [x] 三级角色 + 三级可见性 + usePermission + 用户管理页 + 后端权限注入

#### 帮助页 (REQ-P3-003) ✅
- [x] FAQ 折叠面板 + 404 页面

### 待开始

- [ ] 前端：国际化配置 vue-i18n (REQ-P3-001)
- [ ] 小说详情页 (REQ-P3-005)

---

*本文件由 AI 维护，请勿手动编辑关键部分*

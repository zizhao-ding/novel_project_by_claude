# 项目概况

> **类型**: 全局经验
> **最后更新**: 2026-06-25

## 项目概述

小说在线阅读平台，支持图片和文本小说（TXT）上传及 PC 端在线阅读。

## 目录结构

```
novel_project_by_claude/
├── frontend_project/       # 前端 — Vue 3 + Vite + Element Plus
├── backend_project/        # 后端 — Python FastAPI + SQLite
├── docs/                   # 📚 项目文档 (Harness 架构)
│   ├── index.md            # 总索引
│   ├── requirements/       # 需求文档
│   ├── specs/              # 规范文档
│   │   └── core/           # 核心规范 (启动时必读)
│   └── ai-memory/          # AI 记忆文档
│       ├── global/         # 全局经验
│       └── module/         # 模块经验
├── CLAUDE.md               # AI 开发主入口
└── .claude/                # Claude Code 配置
    └── settings.local.json # 权限和 hooks 配置
```

## 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue 3 (Composition API + `<script setup>`) | ^3.5 |
| 语言 | TypeScript | - |
| 构建 | Vite | ^8.0 |
| UI 库 | Element Plus | - |
| CSS 方案 | UnoCSS + SCSS (BEM 命名) | - |
| 状态管理 | Pinia (Setup Store 模式) | ^3.0 |
| 路由 | Vue Router (懒加载) | ^4.6 |
| HTTP | Axios (统一拦截器封装) | ^1.18 |
| 后端框架 | Python FastAPI | - |
| 数据库 | SQLite + SQLModel | - |
| 认证 | JWT + bcrypt | - |

## 分支策略

```
main                    # 生产分支（只接受 merge，不直接 commit）
├── feature_1.0.0.1     # 版本集成分支
│   ├── feature_zizhao  # 个人功能分支（当前分支）
│   └── feature_xxx     # 其他功能分支
```

**Why:** 每次新对话需了解项目全貌，避免重复询问。

**How to apply:** 新会话启动时，先读取本文件了解项目概况。

**相关记忆**: [[02_ngrok-setup]] [[03_current-progress]] [[04_harness-architecture]]

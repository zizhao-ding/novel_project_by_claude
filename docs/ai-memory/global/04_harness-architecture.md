# 架构演进：Harness → AI Agent 六层架构

> **类型**: 架构演进记录
> **状态**: 旧架构（Harness）已废弃，新架构（AI Agent 原生六层）已就绪
> **最后更新**: 2026-06-30

## 演进时间线

| 日期 | 事件 |
|------|------|
| 2026-06-25 | Harness 六层架构整合完成（旧） |
| 2026-06-30 | 迁移到 AI Agent 原生六层架构（新） |

## 旧架构：Harness 六层（已废弃）

Harness 六层架构是一个**软件工程生命周期流水线**模型：

```
需求层(L1) → 规范层(L2) → 方案层(L3) → 执行层(L4) → 审核层(L5) → 验收层(L6)
```

各层按时间顺序推进，产出需求文档、技术方案、代码、审查报告、测试结果。

## 新架构：AI Agent 原生六层（当前）

AI Agent 原生六层架构是一个**多维度并行治理**模型：

```
规范层 · 上下文层 · 约束层 · 记忆层 · 工具层 · 工作流层
```

六个维度在 AI 的每一次行为中同时生效，而非按时间顺序推进。

**架构总纲**：`docs/specs/core/ai-agent-architecture.md`

## 映射关系

| 旧 Harness | 新架构 |
|-----------|--------|
| L1 需求层 | 上下文层（需求状态）+ 记忆层（需求历史） |
| L2 规范层 | 规范层（编码规则）+ 约束层（Hook 规则） |
| L3 方案层 | 工作流层（方案设计阶段）+ 记忆层（ADR） |
| L4 执行层 | 工具层（代码生成工具） |
| L5 审核层 | 工作流层（审核阶段）+ 约束层（POST 检查） |
| L6 验收层 | 工作流层（验收阶段）+ 上下文层（状态更新） |

## 关键改进

- 上下文层独立 — 启动时统一加载项目状态
- 约束层独立 — 30 条硬性红线与建议性规范分离
- 记忆层一等公民 — ADR、技术债务、踩坑经验有明确归属
- 工具层显式定义 — 能力圈、权限边界、首选工具映射
- 工作流层多样化 — 5 条 SOP（启动/开发/修复/审查/结束）

## 旧整合记录（历史参考）

以下内容来自 2026-06-25 的 Harness 整合，作为历史记录保留：

### 整合完成内容

1. **创建 docs 目录结构**（`requirements/`, `specs/core/`, `specs/detail/`, `specs/module/`, `ai-memory/`）
2. **创建索引文件**（`docs/index.md`, `docs/requirements/index.md`）
3. **迁移需求文档**（从 `spec/` → `docs/requirements/`）
4. **整合规范文档**（11 个 rules 文件 → 3 个核心规范文件）
5. **更新 CLAUDE.md**
6. **清理旧目录**（`.claude/rules/`, `spec/`）

### 整合映射（历史）

| 原文件 | 目标文件 | 状态 |
|--------|----------|------|
| 01_project_structure.md | coding-standards.md | ✅ |
| 02_vue3_components.md | coding-standards.md | ✅ |
| 03_typescript.md | coding-standards.md | ✅ |
| 04_state_management.md | architecture.md | ✅ |
| 05_api_services.md | architecture.md | ✅ |
| 06_styling.md | coding-standards.md | ✅ |
| 07_routing.md | architecture.md | ✅ |
| 08_error_handling.md | architecture.md | ✅ |
| 09_git_conventions.md | coding-standards.md | ✅ |
| 10_progress_tracking.md | architecture.md | ✅ |
| 11_confirm_dialog.md | architecture.md | ✅ |

**Why:** 记录架构演进过程，让未来的 AI 会话理解项目架构的历史脉络和设计意图。

**How to apply:** 新会话启动时按新架构流程加载；本文档仅在需要理解历史决策时查阅。

**相关记忆**: [[03_current-progress]] [[06_architecture-decisions]]

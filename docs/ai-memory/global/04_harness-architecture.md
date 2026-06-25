# Harness 六层架构整合

> **类型**: 项目架构
> **最后更新**: 2026-06-25

## 整合完成

**日期**: 2026-06-25

### 完成内容

1. **创建 docs 目录结构**
   - `docs/requirements/` - 需求文档
   - `docs/specs/core/` - 核心规范
   - `docs/specs/detail/` - 详细规范
   - `docs/specs/module/` - 模块规范
   - `docs/ai-memory/global/` - 全局经验
   - `docs/ai-memory/module/` - 模块经验

2. **创建索引文件**
   - `docs/index.md` - 项目总索引
   - `docs/requirements/index.md` - 需求索引

3. **迁移需求文档**
   - 将 `spec/01_auth_register.md` 迁移到 `docs/requirements/feature-auth-register.md`
   - 添加验收标准和状态字段
   - 创建 `docs/requirements/feature-novel-upload.md`

4. **整合规范文档**
   - 创建 `docs/specs/core/coding-standards.md` - 编码规范（整合 01, 02, 03, 06, 09）
   - 创建 `docs/specs/core/architecture.md` - 架构规范（整合 04, 05, 07, 08, 11 + 进度跟踪）
   - 创建 `docs/specs/core/hook-rules.md` - Hook 规则

5. **更新 CLAUDE.md**
   - 整合 Harness 六层架构
   - 添加启动流程和开发流程
   - 保留项目特色

6. **清理旧目录**
   - 删除 `.claude/rules/` 目录（11 个 rules 文件已整合到 docs/specs/core/）
   - 删除 `spec/` 目录（需求文档已迁移到 docs/requirements/）

### 文档结构

```
docs/
├── index.md                           # 总索引
├── requirements/
│   ├── index.md                       # 需求索引
│   ├── _template.md                   # 需求文档模板
│   ├── feature-auth-register.md       # 用户认证需求 ✅
│   └── feature-novel-upload.md        # 小说上传需求 ✅
└── specs/
    └── core/
        ├── coding-standards.md        # 编码规范（整合 5 个 rules）
        ├── architecture.md            # 架构规范（整合 6 个 rules）
        └── hook-rules.md              # Hook 规则（新建）
```

### 整合映射

| 原文件 | 目标文件 | 状态 |
|--------|----------|------|
| 01_project_structure.md | coding-standards.md | ✅ 已整合 |
| 02_vue3_components.md | coding-standards.md | ✅ 已整合 |
| 03_typescript.md | coding-standards.md | ✅ 已整合 |
| 04_state_management.md | architecture.md | ✅ 已整合 |
| 05_api_services.md | architecture.md | ✅ 已整合 |
| 06_styling.md | coding-standards.md | ✅ 已整合 |
| 07_routing.md | architecture.md | ✅ 已整合 |
| 08_error_handling.md | architecture.md | ✅ 已整合 |
| 09_git_conventions.md | coding-standards.md | ✅ 已整合 |
| 10_progress_tracking.md | architecture.md | ✅ 已整合 |
| 11_confirm_dialog.md | architecture.md | ✅ 已整合 |

### 关键改动

- **启动流程**: 新会话必须读取 `docs/index.md` → `docs/requirements/index.md` → `docs/specs/core/`
- **需求状态**: `pending` → `developing` → `done`
- **Hook 检查**: PreToolUse（工具调用前）+ PostToolUse（工具调用后）
- **验收标准**: 每个需求必须有明确的验收清单
- **进度跟踪**: 整合到 architecture.md 第 7 节

**Why:** 整合 Harness 六层架构，建立标准化的 AI 驱动开发流程。

**How to apply:** 每次新会话启动时，按启动流程读取文档；开发过程中遵循 Hook 检查规则；完成后更新需求状态和验收标准。

**相关记忆**: [[01_project-overview]] [[03_current-progress]]

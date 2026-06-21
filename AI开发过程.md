# AI 开发过程

> 本文档记录前端项目 Rules & Spec 体系的建立过程、文件清单及后续使用方式。

## 一、背景与需求

**用户提问**：

> 现在给这个前端项目制定开发规范，即给这个项目引入 rules 这个概念，通过 spec 和 rule 规范控制前端开发

**需求分析**：

当前项目已有完整的前端编码规范文档（`前端开发规范.md`，760行）和技术选型文档（`技术选型.md`），但缺乏结构化的、可供 AI 辅助开发直接使用的规则和规格体系。需要建立一套 "Rules + Spec" 体系，让 AI 在代码生成、代码审查、功能开发时有明确的规范和约束可遵循。

**核心概念**：

| 概念 | 定义 | 作用 |
|------|------|------|
| **Rule（规则）** | 定义 **HOW** — 怎么写代码 | 持久有效，始终应用于代码生成和审查 |
| **Spec（规格）** | 定义 **WHAT** — 要做什么 | 按功能划分，开发前阅读，开发后归档 |

## 二、生成文件清单

### 项目根目录

| 文件 | 位置 | 说明 |
|------|------|------|
| `CLAUDE.md` | 项目根目录 | 🔑 **主入口文件**，Claude Code 自动加载。包含项目概述、技术栈、规则/规格索引、AI 开发工作流、关键约束速查 |
| `AI开发过程.md` | 项目根目录 | 📝 **本文档**，记录体系建立过程和后续使用方式 |

### 规则目录 `.claude/rules/`

| 文件 | 行数 | 来源 | 内容 |
|------|------|------|------|
| `01_project_structure.md` | 50 | §1 | 目录结构、文件命名（组件 PascalCase / 工具 kebab-case） |
| `02_vue3_components.md` | 100 | §3, §5 | `<script setup>` 标准模板、Props/Emits 定义、事件命名 |
| `03_typescript.md` | 98 | §2 | 接口/类型/枚举命名、泛型规范、避免 any |
| `04_state_management.md` | 98 | §6 | Pinia Setup Store 模式、storeToRefs 解构 |
| `05_api_services.md` | 103 | §7 | Axios 实例封装、拦截器、业务 API 组织 |
| `06_styling.md` | 104 | §9 | BEM 命名、SCSS 组织、Element Plus CSS 变量、UnoCSS |
| `07_routing.md` | 94 | §8 | 路由懒加载、meta 元信息、路由守卫 |
| `08_error_handling.md` | 87 | §10 | 全局错误处理、try-catch-finally、HTTP 错误码 |
| `09_git_conventions.md` | 61 | 新增 | Conventional Commits、分支策略、PR 规范 |

### 规格目录 `spec/`

| 文件 | 行数 | 说明 |
|------|------|------|
| `_template.md` | 128 | 📐 **功能规格模板**，新功能开发前复制此模板填写 |
| `01_auth_register.md` | 204 | 示例：用户注册登录功能规格，含 UI 布局、组件树、数据流、API 契约、验收标准 |

### 已有文件修改

| 文件 | 修改内容 |
|------|----------|
| `前端开发规范.md` | 在文件头部添加了体系索引说明，指向 `.claude/rules/`、`spec/` 和 `CLAUDE.md` |

## 三、设计原则

1. **760行 → 9个 ≤104行 的规则文件**：完整规范文档太长，AI 无法一次性加载。拆分为聚焦领域的小文件，AI 按需加载，每个文件控制在 100 行左右。

2. **编号前缀 `01_`-`09_`**：确保加载顺序和优先级，方便 CLAUDE.md 中引用。

3. **✅ 推荐 vs ❌ 错误**：每个规则文件包含正确和错误的代码示例，直观可操作。

4. **Spec 模板驱动**：所有功能规格遵循 `_template.md` 的统一结构，确保规格的完整性和一致性。

5. **渐进式落地**：先建立框架（CLAUDE.md + rules + spec template），后续开发每个功能时填写对应的 spec 文件。

6. **规范文档转型为「为什么」文档**：`前端开发规范.md` 已从 760 行的代码参考手册精简为 ~180 行的架构决策文档，聚焦设计理由和「为什么这样选」。代码示例部分全部移入 rules 文件。当 rules 与本文档冲突时，以本文档为准。

## 四、后续使用方式

### 4.1 AI 开发工作流

当接到前端开发任务时，AI 按以下流程执行：

```
1. 读取 Spec
   └── 在 spec/ 目录查找对应功能规格，理解需求和验收标准

2. 加载 Rules
   └── 根据任务类型加载相关规则文件
       （至少加载 01_project_structure.md 和 02_vue3_components.md）

3. 遵循规范
   └── 生成代码时严格遵循 rules 中的 ✅ 示例，避免 ❌ 示例

4. 验证一致性
   └── 确保代码风格与已有代码保持一致
```

### 4.2 新功能开发流程

```
Step 1: 创建 Spec
  复制 spec/_template.md → spec/XX_feature_name.md
  填写功能概述、UI 布局、组件树、数据流、API 契约、验收标准

Step 2: AI 阅读 Spec + Rules
  AI 自动读取 CLAUDE.md → 加载相关 rules → 阅读功能 spec

Step 3: AI 生成代码
  遵循 rules 规范生成组件、Store、API 服务、路由等代码

Step 4: 对照验收标准检查
  按 spec 中的 Given-When-Then 场景验证功能完整性
```

### 4.3 新增规则

当需要补充新的编码规范时：

1. 在 `.claude/rules/` 下创建 `XX_rule_name.md`（按编号递增）
2. 遵循现有规则文件的格式：核心原则 + ✅/❌ 示例 + 关键约束
3. 在 `CLAUDE.md` 的规则索引表格中添加新条目
4. 必要时更新 `前端开发规范.md` 作为权威来源

### 4.4 日常使用场景

| 场景 | 操作 |
|------|------|
| **写新组件** | 加载 `01`, `02`, `03`, `06` |
| **写 Store** | 加载 `01`, `03`, `04`, `08` |
| **写 API 服务** | 加载 `01`, `03`, `05`, `08` |
| **写路由** | 加载 `01`, `07` |
| **代码审查** | 加载全部 9 个规则文件 |
| **提交代码** | 参考 `09_git_conventions.md` |

## 五、Memory 记忆系统

### 5.1 为什么需要 Memory

CLAUDE.md 解决「规范怎么定」的问题，但每次新对话 AI 不知道「上次做到哪了」。Memory 是 Claude Code 的跨对话持久化记忆功能，自动按相关性召回。

| | CLAUDE.md | Memory |
|---|---|---|
| **存什么** | 静态规范（技术栈、编码标准） | 动态进度（上次做到哪、待办项） |
| **更新方式** | 手动编辑 | 对话中 `/memory` 命令保存 |
| **变化频率** | 低 | 高 |
| **加载方式** | 全量自动加载 | 按相关性自动召回 |

### 5.2 已创建的 Memory 文件

存储位置：`.claude/projects/-Users-peiwending-Desktop-novel-project-by-claude/memory/`

| 文件 | 内容 |
|------|------|
| `project-overview.md` | 项目概况、技术栈、目录结构 |
| `rules-spec-system.md` | Rules & Spec 体系说明 |
| `current-progress.md` | 当前开发进度（已完成 / 进行中 / 待开始） |
| `frontend-standards-refactor.md` | 规范文档转型记录（768行 → 212行） |

索引文件：`MEMORY.md`（在 memory 目录上级，每次对话自动加载）

### 5.3 使用方式

**后续开发中**：
- 完成一个功能后，对话中说「记录到 Memory：XX 功能已完成」
- 开始新对话时，说「继续上次的开发」，AI 会自动召回相关记忆
- 查看当前进度时，说「我们做到哪了」

**手动管理**：
- 运行 `/memory` 查看和管理已保存的记忆
- 在对话中说「记住 X」自动写入 memory

## 六、文件关系图

```
AI开发过程.md  ← 你在这里（开发过程记录）
    │
    ├── CLAUDE.md  ───────────────────── AI 自动加载的主入口
    │   ├── 引用 → .claude/rules/*.md  ─ 编码规范（HOW）
    │   └── 引用 → spec/*.md           ─ 功能规格（WHAT）
    │
    ├── 前端开发规范.md  ──────────────── 架构决策（WHY）
    │
    ├── Memory 记忆系统 ──────────────── 跨对话进度持久化
    │   ├── MEMORY.md                 ─ 记忆索引（自动加载）
    │   └── memory/*.md               ─ 5条项目记忆
    │
    └── 技术选型.md  ─────────────────── 技术栈和架构决策
```

## 七、ngrok 内网穿透配置

### 背景

手机和电脑连同一 WiFi 时可通过局域网 IP 访问（`http://192.168.x.x:5173`），但要让外网的人也能访问，需要 ngrok。

### 安装

```bash
brew install ngrok
```

### 首次配置

1. https://dashboard.ngrok.com/signup 注册（GitHub 一键登录）
2. 获取 authtoken 并配置：`ngrok config add-authtoken <token>`
3. 遇到 macOS 安全拦截：`sudo xattr -d com.apple.quarantine /opt/homebrew/bin/ngrok`

### 启动

```bash
# 前后端必须先用 --host 启动（后端 8000 + 前端 npx vite --host）
ngrok http 5173 --request-header-add "ngrok-skip-browser-warning:1"
```

终端显示 `www.ngrok-free.dev 网址 -> http://localhost:5173`，把网址发给任何人即可。

### 踩坑记录

| 问题 | 解决 |
|------|------|
| 版本过旧 `ERR_NGROK_121` | `ngrok update` 或官网下载新版 |
| 手机打开显示英文警告页 | 加参数 `--request-header-add "ngrok-skip-browser-warning:1"` |
| Vite 拒绝 ngrok 域名 403 | `vite.config.ts` 加 `allowedHosts: ['.ngrok-free.dev']` |

### 已修改文件

- `front_project/vite.config.ts` — 添加 `allowedHosts`
- `memory/ngrok-setup.md` — 完整配置指南
- `MEMORY.md` — 已索引

## 八、关键约束速查

以下规则 **不可违反**：

- ✅ **必须使用 TypeScript**，所有 `.vue` 文件使用 `<script setup lang="ts">`
- ✅ **必须使用 Element Plus** 作为 UI 组件库，禁止引入其他 UI 库
- ✅ **必须使用 Composition API**（`ref`, `computed`, `watch` 等），禁止 Options API
- ✅ **必须使用 Pinia Setup Store** 模式
- ✅ **必须使用 BEM 命名** 编写自定义样式
- ✅ 路由组件**必须懒加载**（`() => import(...)`）
- ✅ 所有异步操作**必须有错误处理**
- ❌ 禁止使用 `var`、`==`（使用 `const`/`let`、`===`）
- ❌ 禁止在模板中使用复杂表达式（抽取为 `computed`）
- ❌ 禁止直接操作 DOM（使用 Vue 响应式绑定）

# CLAUDE.md — AI Agent 运行时配置

> 我是这个**小说在线阅读平台**的 AI 开发助手。以下六层治理框架定义了我在本项目中的行为准则、能力边界和执行方式。
>
> 架构总纲详见：`docs/specs/core/ai-agent-architecture.md`

---

## ━━━ 上下文层：现在在做什么 ━━━

### 项目概述

- **项目名称**：小说阅读平台
- **项目类型**：全栈应用（Vue 3 前端 + Python FastAPI 后端）
- **当前阶段**：开发中 — Phase 3 功能完善
- **当前分支**：`feature_zizhao`

### 技术栈

| 类别 | 技术 | 说明 |
|------|------|------|
| 框架 | Vue 3 (Composition API + `<script setup>`) | 强制使用 |
| 语言 | **TypeScript**（强制，禁止纯 JS） | 严格模式 |
| 构建 | Vite ^8.0 | |
| UI 库 | **Element Plus**（按需导入） | 禁止其他 UI 库 |
| CSS 方案 | UnoCSS + SCSS (BEM 命名) | |
| 状态管理 | Pinia (Setup Store 模式) | |
| 路由 | Vue Router (懒加载) | |
| HTTP | Axios (统一拦截器) | |
| 国际化 | vue-i18n ^11.4 | |
| 后端 | Python FastAPI + SQLite + SQLModel | |

### 需求状态速览

| 状态 | 数量 |
|------|------|
| ✅ 已完成 | 9 个 (REQ-P1-001~002, P2-001~003, P3-002~004) |
| 📝 待处理 | 2 个 (REQ-P3-001 国际化, REQ-P3-005 小说详情页) |

详见：`docs/requirements/index.md`

### 启动时必读文件

```
1. docs/index.md                                   → 项目全貌
2. docs/requirements/index.md                      → 需求状态
3. docs/ai-memory/global/03_current-progress.md    → 当前进度
4. docs/ai-memory/global/06_architecture-decisions.md → 架构决策
```

---

## ━━━ 约束层：绝对不能做的事 ━━━

以下规则**不可违反**，违反即错误。详细定义：`docs/specs/core/constraint-layer.md`

### 技术栈红线

- ✅ **必须使用 TypeScript**，所有 `.vue` 文件 `<script setup lang="ts">`
- ✅ **必须使用 Element Plus** 作为唯一 UI 组件库
- ✅ **必须使用 Composition API**（`ref`, `computed`, `watch` 等），禁止 Options API
- ✅ **必须使用 Pinia Setup Store**（`defineStore('name', () => { ... })`）
- ✅ **路由组件必须懒加载**（`() => import(...)`）

### 代码红线

- ❌ 禁止 `var`、`==`（使用 `const`/`let`、`===`）
- ❌ 禁止 `any`（使用 `unknown` + 类型守卫）
- ❌ 禁止在模板中使用复杂表达式（抽取为 `computed`）
- ❌ 禁止直接操作 DOM（使用 Vue 响应式绑定）
- ❌ 禁止 `@ts-ignore`（使用 `@ts-expect-error`）

### 架构红线

- ❌ 禁止组件中直接使用 `axios`/`fetch`（统一通过 `services/` + `api.client`）
- ❌ 禁止跨层级相对路径（使用 `@` 别名）
- ❌ 禁止 Store 中调用 UI 组件（`ElMessageBox` 等放在视图层 — ADR-004）
- ❌ 禁止 Store state 直接修改（必须通过 action）

### 安全红线

- ❌ 禁止 `v-html` 渲染用户输入（XSS 风险）
- ❌ 删除操作必须 `ElMessageBox.confirm` 二次确认
- ❌ 所有异步操作必须有 `try-catch` 错误处理
- ❌ 禁止空 `catch` 块吞掉错误

### 流程红线

- ❌ 提交前必须通过 ESLint + TypeScript 检查
- ❌ 禁止 `git push --force` 到共享分支
- ❌ 会话结束必须更新进度记录
- ❌ 每次问题解决后必须本地 commit（Conventional Commits 格式，不push）

---

## ━━━ 规范层：代码质量标准 ━━━

### 编码规范速查

详见：`docs/specs/core/coding-standards.md`

**文件命名**：

| 文件类型 | 命名 | 示例 |
|---------|------|------|
| Vue 组件 | PascalCase | `UserCard.vue` |
| 视图文件 | `*View.vue` | `HomeView.vue` |
| TS 工具 | kebab-case | `format-date.ts` |
| Store | 名词单数 | `user.ts` |
| 类型定义 | kebab-case | `novel.ts` |

**组件标准模板**：

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

interface Props { title: string; disabled?: boolean; }
const props = withDefaults(defineProps<Props>(), { disabled: false });

const emit = defineEmits<{ (e: 'item-click', id: number): void }>();

const internalValue = ref('');
const isValid = computed(() => internalValue.value.length > 0);

function handleChange(value: string) {
  internalValue.value = value;
  emit('value-change', value);
}
</script>

<template>
  <div class="component-name"><!-- 用 computed，不用复杂表达式 --></div>
</template>

<style scoped lang="scss">
.component-name { /* BEM 命名 */ }
</style>
```

**SCSS BEM 命名**：

```scss
.component-name {
  &__element { }       // 元素：__ 双下划线
  &--modifier { }      // 修饰符：-- 双连字符
}
```

**Git Commit**：`<type>(<scope>): <subject>` — type: feat/fix/docs/refactor/chore

### 架构规范速查

详见：`docs/specs/core/architecture.md`

**Pinia Store 标准结构**：

```typescript
export const useXxxStore = defineStore('xxx', () => {
  // ── State ──
  const items = ref<Item[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  // ── Getters ──
  const itemCount = computed(() => items.value.length);
  // ── Actions ──
  async function fetchItems() {
    loading.value = true; error.value = null;
    try { items.value = await api.getList(); }
    catch (err) { error.value = (err as Error).message; }
    finally { loading.value = false; }
  }
  return { items, loading, error, itemCount, fetchItems };
});
```

**组件中使用 Store**：

```typescript
const store = useXxxStore();
const { items, loading } = storeToRefs(store);  // ✅ 必须 storeToRefs
const { fetchItems } = store;                     // ✅ actions 直接解构
```

**API 服务层**：统一通过 `services/api.ts` 的 Axios 实例，业务 API 按领域分文件（`auth.ts`, `novel.ts` 等）

---

## ━━━ 工具层：能力边界 ━━━

### 首选工具映射

| 任务 | 工具 | 非 |
|------|------|-----|
| 读文件 | `Read` | `cat` |
| 写新文件 | `Write` | `echo >` |
| 修改文件片段 | `Edit` | `sed` |
| 搜索文件 | `Glob` | `ls` / `find` |
| 搜索代码 | `Grep` | `grep` |
| 运行命令 | `Bash` | — |
| 复杂多步骤任务 | `Agent` | — |
| 需要用户决策 | `AskUserQuestion` | — |

### 权限边界

- **自主执行**：读项目文件、修改项目文件、运行 lint/type-check、搜索代码、创建文档
- **需要确认**：删除文件、修改配置、git push、安装依赖、危险命令
- **不能执行**：force push 共享分支、绕过 Hook 提交、违反约束层规则

### 常用命令

```bash
cd frontend_project && npm run dev      # 启动前端
cd backend_project && python -m uvicorn app.main:app --reload  # 启动后端
cd frontend_project && npm run build    # 构建
cd frontend_project && npm run lint     # ESLint
cd frontend_project && npm run format   # Prettier
```

---

## ━━━ 记忆层：过去学到的 ━━━

### 关键架构决策

| ADR | 决策要点 |
|-----|---------|
| ADR-001 | 权限系统：纯 visibility 字段控制，书架回归收藏夹 |
| ADR-002 | AppHeader：全局统一顶栏，8+ 页面统一使用 |
| ADR-003 | 阅读器：三主题 + 进度自动保存 |
| ADR-004 | 敏感操作确认：在视图层调用 ElMessageBox，不在 Store |
| ADR-005 | 后端权限：FastAPI Depends 函数式注入 |

详见：`docs/ai-memory/global/06_architecture-decisions.md`

### 技术债务

- 测试覆盖率不足：前端 ~15%，后端 ~35%
- 详见：`docs/ai-memory/global/05_testing-debt.md`

### 项目特有约定

- Vite 8 + Rolldown：`resolve.alias` 构建不生效，dev server 可用 `@` 别名
- Element Plus：`ElMessage` 通过 `unplugin-auto-import` 自动注入
- SCSS：使用 `sass`（非 `sass-embedded`，macOS 12 兼容性）
- ESLint：扁平配置 `eslint.config.js`（v9 格式）

---

## ━━━ 工作流层：按什么流程做 ━━━

### 会话启动流程（自动执行）

```
1. 读取 docs/index.md — 了解项目全貌
2. 读取 docs/requirements/index.md — 获取需求状态
3. 读取 docs/specs/core/constraint-layer.md — 加载红线
4. 读取 docs/ai-memory/global/03_current-progress.md — 当前进度
5. 读取 docs/ai-memory/global/06_architecture-decisions.md — 架构决策
6. 扫描待处理需求 → 提示用户确认开发目标
```

### 标准开发流程

```
需求分析 → 方案设计 → 代码实现 → 审核检查 → 验收完成
   │           │           │           │           │
   │           │           │           │           └── git commit + 更新进度 + 沉淀记忆
   │           │           │           └── Lint + TypeCheck + 对照约束层
   │           │           └── 遵循规范层 + 约束层实时检查
   │           └── 查阅记忆层 ADR + 设计方案
   └── 加载上下文层需求文档
```

### 快速修复流程

```
定位问题 → 确认方案(不违反红线) → Edit 修改 → Lint/TypeCheck 验证 → git commit → 完成
```

### 代码审查流程

```
加载代码 → 对照规范层 → 对照约束层 → 对照记忆层 → 输出报告
```

### 会话结束流程

```
1. 更新 03_current-progress.md — checkbox 状态
2. 更新需求文档状态标签 — pending/developing/done
3. 如有值得记录的经验 → 写入记忆层
4. 如有重大决策 → 补充 ADR
5. git add + git commit — Conventional Commits 格式，记录本次会话成果
```

---

## ━━━ 项目结构 ━━━

```
novel_project_by_claude/
├── CLAUDE.md                           # 本文件 — AI Agent 运行时入口
├── frontend_project/                   # 前端 (Vue 3 + Element Plus)
│   └── src/
│       ├── components/{base,business,ui}/
│       ├── views/        # *View.vue 页面（懒加载）
│       ├── router/       # 路由 + 守卫
│       ├── stores/       # Pinia Setup Store
│       ├── services/     # API 封装 (api.ts + 业务模块)
│       ├── composables/  # Vue Composables
│       ├── types/        # TypeScript 类型
│       ├── utils/        # 纯工具函数
│       └── constants/    # 常量
├── backend_project/                   # 后端 (FastAPI + SQLite)
└── docs/                              # 文档（六层架构）
    ├── index.md                       #   总索引
    ├── specs/core/                    #   规范层 + 约束层
    ├── specs/detail/                  #   详细规范
    ├── specs/module/                  #   模块规范
    ├── requirements/                  #   需求文档
    └── ai-memory/                     #   记忆层
```

---

*本文件由 AI 维护，是 AI Agent 在本项目中的运行时配置入口*
*架构总纲：`docs/specs/core/ai-agent-architecture.md`*

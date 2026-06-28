# 代码审核规范

> **优先级**: P1 - 应该遵守
> **最后更新**: 2026-06-28
> **关联层级**: Harness Layer 5 — 审核层

## 1. 审核流程

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 自检     │ →  │ ESLint   │ →  │ TS 检查   │ →  │ 人工审核  │
│ (开发者)  │    │ (自动)    │    │ (自动)    │    │ (AI/人)  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### 执行命令

```bash
# 自动检查
cd frontend_project && npm run lint        # ESLint
cd frontend_project && npm run type-check  # TypeScript

# 后端检查
cd backend_project && python -m pytest tests/ -v  # 后端测试
```

## 2. 代码审核清单

### 2.1 规范合规 (P0)

- [ ] 文件使用 `<script setup lang="ts">`
- [ ] 使用 Composition API（ref/computed/watch）
- [ ] Props 使用 TypeScript 接口定义（非运行时对象）
- [ ] Emits 使用 TypeScript 元组签名
- [ ] Store 使用 Setup Store 模式
- [ ] Store 解构使用 `storeToRefs`
- [ ] 路由组件使用懒加载 `() => import(...)`
- [ ] 使用 `@` 别名导入（非相对路径 `../../../`）
- [ ] 未引入禁止依赖（antd、lodash 等替代 UI 库）

### 2.2 类型安全 (P1)

- [ ] 无 `any` 类型（除非有明确理由并注释）
- [ ] 无 `as` 强制类型断言（除非有充分理由）
- [ ] API 响应有泛型类型标注
- [ ] 函数参数和返回值有类型标注
- [ ] 无 `// @ts-ignore` 或 `// @ts-nocheck`

### 2.3 错误处理 (P1)

- [ ] 所有 `async/await` 有 `try-catch`
- [ ] catch 块有用户可见提示（ElMessage）
- [ ] 无可吞掉错误的空 catch 块
- [ ] 敏感操作有 `ElMessageBox.confirm` 二次确认
- [ ] 确认文案说明操作后果（如"不可恢复"）

### 2.4 安全 (P0)

- [ ] 无 `v-html` 直接渲染用户输入（XSS 风险）
- [ ] 无硬编码的 token/密码/密钥
- [ ] 无 `console.log` 打印敏感信息
- [ ] 前端不存储明文密码

### 2.5 性能 (P2)

- [ ] 大列表使用分页或虚拟滚动
- [ ] 无在 `watch`/`computed` 中执行重操作
- [ ] 事件监听在 `onBeforeUnmount` 中移除
- [ ] 图片使用懒加载（如需要）

### 2.6 可维护性 (P1)

- [ ] 无重复的工具函数（应放在 `utils/`）
- [ ] 无重复的类型定义（应放在 `types/`）
- [ ] 组件职责单一，不超过 300 行
- [ ] 复杂的 computed 有注释说明
- [ ] 魔法数字提取为常量

### 2.7 文档同步 (P1)

- [ ] 新增功能：对应需求文档验收标准已勾选
- [ ] 新增组件/Store/API：已在模块规范中记录
- [ ] 架构决策：已在 06_architecture-decisions.md 补充 ADR
- [ ] 进度变更：已更新 03_current-progress.md

## 3. 审核严重级别

| 级别 | 标签 | 处理 |
|------|------|------|
| P0 阻断 | `[blocker]` | 必须修复才能合并 |
| P1 重要 | `[major]` | 应修复，有充分理由可豁免 |
| P2 建议 | `[minor]` | 建议修复，不阻塞合并 |

## 4. 自动审核集成

### Git PreCommit Hook

```bash
# .husky/pre-commit 已配置
npx prettier --write .
```

### ESLint 规则

```javascript
// eslint.config.js 已配置
// - Vue 3 强推荐规则
// - TypeScript 严格规则
// - Prettier 格式化对齐
```

### 未来可集成

- [ ] pre-push hook：运行测试套件
- [ ] CI pipeline：ESLint + TypeCheck + Test
- [ ] PR 模板：包含审核清单 checkbox

## 5. 审核记录模板

每次审核完成后，可选记录摘要：

```markdown
## Review-YYYYMMDD-001

**日期**: 2026-06-28
**范围**: ReaderView.vue + stores/reader.ts
**审核人**: AI (Claude)

### 发现
- [blocker] xxx — 已修复于 commit xxxxxx
- [major] xxx — 已修复
- [minor] xxx — 记录为技术债务

### 结论
✅ 通过 / ⚠️ 有条件通过 / ❌ 需重新审核
```

## 6. 质量度量

### 当前基线 (2026-06-28)

| 指标 | 当前 | 目标 |
|------|------|------|
| TypeScript 覆盖率 | ~100% | 100% |
| ESLint 通过率 | ✅ 通过 | 保持 |
| 前端测试覆盖率 | <5% | ≥80% ⚠️ |
| 后端测试覆盖率 | <20% | ≥90% ⚠️ |
| 类型重复定义 | 4 处 | 0 |
| 工具函数重复 | formatSize/formatDate 4处 | 0 |

### 改进路线

1. **短期（1-2 轮）**: 清理类型重复 + 工具函数集中化
2. **中期（3-5 轮）**: 补充后端 API 测试到 60%+
3. **长期**: 达到前端 80% / 后端 90% 测试覆盖

---

**Why:** Layer 5 审核层需要明确的检查标准和流程，确保每次代码变更都经过质量把关。

**How to apply:** 每次功能开发完成或 PR 合并前，按审核清单逐项检查。

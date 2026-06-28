# 工具链使用指南

## 📦 已安装的工具

| 工具 | 版本 | 作用 |
|------|------|------|
| TypeScript | ^6.0.3 | 类型检查 |
| ESLint | ^10.6.0 | 代码质量检查 |
| Prettier | ^3.8.4 | 代码格式化 |
| vue-tsc | ^3.3.5 | Vue + TypeScript 类型检查 |

## 🚀 常用命令

### 开发时

```bash
# 启动开发服务器
npm run dev

# 类型检查（不生成文件）
npm run type-check

# ESLint 检查
npm run lint:check

# ESLint 自动修复
npm run lint

# Prettier 格式化
npm run format

# 检查格式是否正确
npm run format:check
```

### 提交前

```bash
# 完整检查流程
npm run type-check && npm run lint:check && npm run format:check

# 自动修复可修复的问题
npm run lint && npm run format
```

### 构建

```bash
# 生产构建
npm run build

# 预览构建结果
npm run preview
```

## 📝 配置文件说明

### tsconfig.json
- **strict**: 启用严格类型检查
- **noUnusedLocals**: 未使用的变量报错
- **noUnusedParameters**: 未使用的参数报错
- **noFallthroughCasesInSwitch**: switch 语句必须 break
- **noUncheckedIndexedAccess**: 数组/对象索引访问可能为 undefined

### eslint.config.js
- **Vue 3 规则**: 强制 Vue 3 最佳实践
- **TypeScript 规则**: 类型安全检查
- **Prettier 集成**: 避免格式冲突
- **自定义规则**:
  - `no-var`: 禁止使用 var
  - `eqeqeq`: 强制使用 ===
  - `no-console`: 警告 console（生产环境应移除）
  - `no-restricted-globals`: 禁止直接使用 document/window

### .prettierrc
- **printWidth**: 140 字符换行
- **singleQuote**: 使用单引号
- **semi**: 使用分号
- **trailingComma**: 尾逗号

## 🔧 IDE 配置（VSCode）

### 推荐扩展
1. **ESLint** (`dbaeumer.vscode-eslint`)
2. **Prettier** (`esbenp.prettier-vscode`)
3. **Vue - Official** (`Vue.volar`)

### settings.json 配置
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

## ⚠️ 当前已知问题

运行 `npm run lint:check` 会发现一些现有代码问题：

### 需要手动修复的错误
1. **`no-useless-assignment`**: 无用的变量赋值
2. **`no-restricted-globals`**: 在非 Vue 文件中使用了 document/window
3. **`@typescript-eslint/no-unused-vars`**: 未使用的变量

### 可接受的警告
1. **`no-console`**: 开发时使用的 console（提交前应移除）
2. **`no-undef`**: 某些全局变量未声明

## 📚 最佳实践

### 写代码时
1. 让 IDE 实时显示错误（安装扩展后自动生效）
2. 保存时自动格式化（配置 settings.json 后）
3. 发现红色波浪线立刻修复

### 提交前
```bash
# 1. 类型检查
npm run type-check

# 2. 代码检查
npm run lint

# 3. 格式化
npm run format

# 4. 构建验证
npm run build
```

### 遇到 ESLint 错误
```bash
# 尝试自动修复
npm run lint

# 如果无法自动修复，手动修改
# 查看错误详情
npm run lint:check

# 修改后再次检查
npm run lint:check
```

## 🎯 规则说明

### 为什么禁止 `var`？
- `var` 有变量提升，容易产生 bug
- `const`/`let` 有块级作用域，更安全

### 为什么强制 `===`？
- `==` 会进行类型转换，产生意外结果
- `===` 严格比较，更可预测

### 为什么警告 `console`？
- 开发时可以用，但生产环境应移除
- 避免泄露敏感信息

### 为什么禁止直接操作 DOM？
- Vue 通过响应式系统管理 DOM
- 直接操作会导致状态不一致
- 使用 Vue 的 ref 和模板绑定

---

*配置完成于 2026-06-28*

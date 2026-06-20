# 09 — Git 提交 & 分支规范

## 分支策略

```
main                    # 生产分支（只接受 merge，不直接 commit）
├── feature_1.0.0.1     # 版本集成分支
│   ├── feature_zizhao  # 个人功能分支（当前分支）
│   └── feature_xxx     # 其他功能分支
```

## Commit 规范（Conventional Commits）

```
<type>(<scope>): <subject>
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(novel): 添加小说上传组件` |
| `fix` | Bug 修复 | `fix(reader): 修复翻页时内容丢失` |
| `docs` | 文档变更 | `docs(rules): 添加组件开发规范` |
| `style` | 代码格式 | `style: 统一缩进为2空格` |
| `refactor` | 重构 | `refactor(api): 重构请求拦截器` |
| `perf` | 性能优化 | `perf(list): 添加虚拟滚动` |
| `test` | 测试相关 | `test(store): 添加 novel store 测试` |
| `chore` | 构建/工具 | `chore: 添加 ESLint 配置` |

### Scope 范围

常用：`auth`, `novel`, `reader`, `library`, `upload`, `router`, `store`, `api`, `style`, `rules`, `spec`

### 示例

```bash
# ✅ 好的 commit
git commit -m "feat(novel): 添加小说列表分页功能"
git commit -m "fix(reader): 修复页面刷新后阅读位置丢失"

# ❌ 不好的 commit
git commit -m "update code"
git commit -m "修改了一些东西"
git commit -m "WIP"
```

## 工作流程

1. 从集成分支创建个人功能分支
2. 在个人分支上开发，保持小步提交
3. 完成后发起 PR 合并到集成分支
4. 代码审查通过后合并

## ✅ 规则速查

- ✅ Commit message 使用英文简要描述
- ✅ 一个 commit 只做一件事
- ✅ 提交前确保代码可以运行
- ❌ 禁止 `git push --force` 到共享分支
- ❌ 禁止提交 `console.log` 调试代码

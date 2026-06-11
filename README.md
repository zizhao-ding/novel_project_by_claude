# novel_project_by_claude

sdd and harness to build

---

## 📋 项目信息

**项目名称**: novel_project_by_claude  
**创建日期**: 2026-06-11  
**仓库地址**: https://github.com/zizhao-ding/novel_project_by_claude

---

## 🌳 分支管理

### 分支结构

```
feature_zizhao (个人开发分支)
        ↓
        合并到
        ↓
feature_1.0.0.1 (版本分支)
        ↓
        合并到
        ↓
main (主分支)
```

### 分支说明

| 分支名 | 用途 | 说明 |
|--------|------|------|
| `main` | 生产发布分支 | 稳定版本，随时可发布 |
| `feature_1.0.0.1` | 版本开发分支 | 1.0.0.1 版本的所有功能集成 |
| `feature_zizhao` | 个人开发分支 | 个人开发工作，定期合并到版本分支 |

---

## 📖 开发工作流程

### 第一步：个人开发（在 feature_zizhao 分支）

```bash
# 切换到个人开发分支
git checkout feature_zizhao

# 进行开发
# 编辑文件...

# 提交更改
git add .
git commit -m "feat(功能): 功能描述"

# 推送到远程
git push
```

### 第二步：同步其他开发者的最新代码

```bash
# 获取远程最新代码
git fetch origin

# 同步版本分支的最新代码（避免冲突）
git rebase origin/feature_1.0.0.1
```

### 第三步：合并到版本分支

```bash
# 切换到版本分支
git checkout feature_1.0.0.1

# 更新版本分支
git pull

# 合并个人开发分支
git merge feature_zizhao

# 推送到远程
git push
```

**或使用 Pull Request**（推荐用于代码审查）：
1. 在 GitHub 上创建 PR：`feature_zizhao` → `feature_1.0.0.1`
2. 进行代码审查
3. 批准后点击 Merge

### 第四步：版本分支合并到主分支（发布）

```bash
# 切换到主分支
git checkout main

# 更新主分支
git pull

# 合并版本分支
git merge feature_1.0.0.1

# 推送到远程（发布）
git push
```

---

## 📚 常用 Git 命令

### 分支操作

```bash
# 查看所有分支
git branch -a

# 切换分支
git checkout <分支名>

# 创建并切换分支
git checkout -b <分支名>

# 推送分支到远程
git push -u origin <分支名>

# 删除本地分支
git branch -d <分支名>

# 删除远程分支
git push origin --delete <分支名>
```

### 提交操作

```bash
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "type(scope): description"

# 推送到远程
git push

# 拉取最新代码
git pull
```

### 同步和合并

```bash
# 获取远程更新
git fetch origin

# 变基当前分支到目标分支
git rebase origin/<分支名>

# 合并分支
git merge <分支名>

# 查看分支之间的差异
git diff <分支1>..<分支2>
```

---

## 💡 开发建议

1. **定期同步**：经常运行 `git fetch origin` 和 `git rebase` 保持与版本分支同步
2. **小颗粒提交**：将功能分解为多个小提交，便于审查和回滚
3. **规范提交信息**：遵循 `type(scope): description` 的格式
4. **代码审查**：使用 Pull Request 进行代码审查
5. **文档记录**：在 [git_project_resolve.md](git_project_resolve.md) 中记录解决的 Git 问题

---

## 🔍 常见问题解决

详见 [git_project_resolve.md](git_project_resolve.md)：
- 无法推送代码到远程仓库
- 创建功能分支工作流
- 分支重命名
- 多层级分支开发流程

---

## 📝 提交信息规范

遵循 Conventional Commits 规范：

```
type(scope): subject

body

footer
```

**类型**：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 其他

**示例**：
```bash
git commit -m "feat(auth): implement user login

- Add login API endpoint
- Implement JWT token generation
- Add password validation"
```

---

## 📋 项目信息

**项目名称**: novel_project_by_claude  
**创建日期**: 2026-06-11  
**仓库地址**: https://github.com/zizhao-ding/novel_project_by_claude

---

## 🌳 分支管理

### 分支结构

```
feature_zizhao (个人开发分支)
        ↓
        合并到
        ↓
feature_1.0.0.1 (版本分支)
        ↓
        合并到
        ↓
main (主分支)
```

### 分支说明

| 分支名 | 用途 | 说明 |
|--------|------|------|
| `main` | 生产发布分支 | 稳定版本，随时可发布 |
| `feature_1.0.0.1` | 版本开发分支 | 1.0.0.1 版本的所有功能集成 |
| `feature_zizhao` | 个人开发分支 | 个人开发工作，定期合并到版本分支 |

---

## 📖 开发工作流程

### 第一步：个人开发（在 feature_zizhao 分支）

```bash
# 切换到个人开发分支
git checkout feature_zizhao

# 进行开发
# 编辑文件...

# 提交更改
git add .
git commit -m "feat(功能): 功能描述"

# 推送到远程
git push
```

### 第二步：同步其他开发者的最新代码

```bash
# 获取远程最新代码
git fetch origin

# 同步版本分支的最新代码（避免冲突）
git rebase origin/feature_1.0.0.1
```

### 第三步：合并到版本分支

```bash
# 切换到版本分支
git checkout feature_1.0.0.1

# 更新版本分支
git pull

# 合并个人开发分支
git merge feature_zizhao

# 推送到远程
git push
```

**或使用 Pull Request**（推荐用于代码审查）：
1. 在 GitHub 上创建 PR：`feature_zizhao` → `feature_1.0.0.1`
2. 进行代码审查
3. 批准后点击 Merge

### 第四步：版本分支合并到主分支（发布）

```bash
# 切换到主分支
git checkout main

# 更新主分支
git pull

# 合并版本分支
git merge feature_1.0.0.1

# 推送到远程（发布）
git push
```

---

## 📚 常用 Git 命令

### 分支操作

```bash
# 查看所有分支
git branch -a

# 切换分支
git checkout <分支名>

# 创建并切换分支
git checkout -b <分支名>

# 推送分支到远程
git push -u origin <分支名>

# 删除本地分支
git branch -d <分支名>

# 删除远程分支
git push origin --delete <分支名>
```

### 提交操作

```bash
# 查看状态
git status

# 添加文件
git add .

# 提交更改
git commit -m "type(scope): description"

# 推送到远程
git push

# 拉取最新代码
git pull
```

### 同步和合并

```bash
# 获取远程更新
git fetch origin

# 变基当前分支到目标分支
git rebase origin/<分支名>

# 合并分支
git merge <分支名>

# 查看分支之间的差异
git diff <分支1>..<分支2>
```

---

## 💡 开发建议

1. **定期同步**：经常运行 `git fetch origin` 和 `git rebase` 保持与版本分支同步
2. **小颗粒提交**：将功能分解为多个小提交，便于审查和回滚
3. **规范提交信息**：遵循 `type(scope): description` 的格式
4. **代码审查**：使用 Pull Request 进行代码审查
5. **文档记录**：在 [git_project_resolve.md](git_project_resolve.md) 中记录解决过的 Git 问题

---

## 🔍 常见问题解决

详见 [git_project_resolve.md](git_project_resolve.md)：
- 无法推送代码到远程仓库
- 创建功能分支工作流
- 分支重命名
- 多层级分支开发流程

---

## 📝 提交信息规范

遵循 Conventional Commits 规范：

```
type(scope): subject

body

footer
```

**类型**：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 其他

**示例**：
```bash
git commit -m "feat(auth): implement user login

- Add login API endpoint
- Implement JWT token generation
- Add password validation"
```

# 小说阅读平台

支持 TXT 小说上传及在线阅读的 PC 端 Web 应用。

> GitHub: https://github.com/zizhao-ding/novel_project_by_claude

---

## 🚀 启动指南

### 环境要求

| 组件 | 要求 |
|------|------|
| Node.js | 18+ |
| Python | 3.9+ |
| macOS | `brew` 已安装 |
| 包管理 | `pip3`（Python）、`npm`（Node） |

### 1. 启动后端

```bash
cd backend_project

# 首次运行：安装依赖
pip3 install -r requirements.txt

# 配置环境变量（首次）
cp .env.example .env

# 启动（http://localhost:8000）
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

启动后访问 http://localhost:8000/docs 查看 Swagger API 文档。

> Windows 用户：使用 `python` 代替 `python3`，`pip` 代替 `pip3`。

### 2. 启动前端

```bash
cd front_project

# 首次运行：安装依赖
npm install

# 启动（http://localhost:5173）
npx vite --host
```

前端 Vite 已配置代理，`/api` 请求自动转发到后端 `localhost:8000`。

### 3. 暴露外网（ngrok）

让没有连同一 WiFi 的人也能访问。前提：已完成 [ngrok 注册](https://dashboard.ngrok.com/signup) 和 authtoken 配置。

```bash
# 安装（首次）
brew install ngrok

# 启动（前后端必须已运行）
ngrok http 5173 --request-header-add "ngrok-skip-browser-warning:1"
```

把终端显示的 `https://xxxx.ngrok-free.dev` 链接发给任何人即可访问。

> 踩坑记录详见 `memory/ngrok-setup.md`

### 一键启动脚本（终端分三窗口）

```bash
# 窗口1：后端
cd backend_project && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 窗口2：前端
cd front_project && npx vite --host

# 窗口3：外网隧道（可选）
ngrok http 5173 --request-header-add "ngrok-skip-browser-warning:1"
```

---

## 📋 Git 使用技巧

### 第一次使用（克隆项目）

```bash
git clone https://github.com/zizhao-ding/novel_project_by_claude.git
cd novel_project_by_claude
git checkout feature_zizhao
```

### 日常开发

```bash
# 查看状态
git status

# 提交三部曲
git add .
git commit -m "feat(模块): 做了什么"
git push
```

### 分支操作

```bash
git branch -a                  # 查看所有分支
git checkout <分支名>           # 切换分支
git checkout -b <分支名>        # 创建并切换新分支
```

### 同步最新代码

```bash
git pull                       # 拉取当前分支最新代码
git fetch origin               # 获取所有远程更新
```

### 查看改动

```bash
git diff                       # 查看未暂存的改动
git log --oneline -10          # 查看最近 10 条提交
```

### Commit 格式

```bash
git commit -m "feat(模块): 简短的改动描述"
```

类型：`feat` 新功能 | `fix` 修bug | `docs` 文档 | `style` 格式 | `refactor` 重构 | `chore` 其他

### 合并流程

```
feature_zizhao → feature_1.0.0.1 → main
```

```bash
# 1. 合并到版本分支
git checkout feature_1.0.0.1
git pull
git merge feature_zizhao
git push

# 2. 合并到主分支（发布）
git checkout main
git pull
git merge feature_1.0.0.1
git push
```

> 推荐用 GitHub Pull Request 做代码审查后再合并。

---

## 📁 项目结构

```
novel_project_by_claude/
├── front_project/              # Vue 3 前端
│   ├── src/views/              #   页面视图
│   ├── src/stores/             #   Pinia 状态
│   ├── src/services/           #   API 服务层
│   ├── src/router/             #   路由
│   └── vite.config.ts          #   Vite 配置（代理 + 别名）
├── backend_project/            # FastAPI 后端
│   ├── app/api/auth.py         #   认证接口
│   ├── app/models/             #   数据模型
│   ├── app/schemas/            #   Pydantic 模型
│   └── .env                    #   环境变量
├── .claude/rules/              # AI 编码规则（9个文件）
├── spec/                       # 功能规格文档
├── CLAUDE.md                   # AI 开发主入口
├── AI开发过程.md                # AI 开发记录
└── 技术选型.md                  # 技术选型文档
```

---

## 🔧 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus + Pinia |
| 后端 | Python FastAPI + SQLModel + SQLite |
| 认证 | bcrypt + JWT (python-jose) |
| 工具 | Prettier + ngrok |

---

## 💾 查看 Memory 进度记录

项目使用 Claude Code 的 Memory 系统记录开发进度，跨对话持久化。

**快速打开**：

```bash
open /Users/peiwending/.claude/projects/-Users-peiwending-Desktop-novel-project-by-claude
```

或者在 Finder 中手动导航：按 `Cmd + Shift + .` 显示隐藏文件 → 进入 `.claude` → `projects` → `-Users-peiwending-Desktop-novel-project-by-claude` → `memory`

文件按创建时间编号：`01_project-overview.md` `02_rules-spec-system.md` `03_ngrok-setup.md` `04_current-progress.md` `05_frontend-standards-refactor.md`

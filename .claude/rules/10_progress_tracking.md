# 10 — 进度记录规范

## 核心原则

每次开发任务完成后，**必须**更新项目进度记录，确保下次新对话能无缝接续。

## Memory 文件命名规范

新建 memory 文件时，使用 **数字前缀 + kebab-case**：

```
01_project-overview.md        # 按创建时间编号
02_rules-spec-system.md
03_ngrok-setup.md
04_current-progress.md
05_frontend-standards-refactor.md
06_xxx.md                     # 后续新文件按序号递增
```

- 数字按创建时间先后分配
- 文件名用 kebab-case（小写 + 连字符）
- 创建后同步更新 `MEMORY.md` 索引

## 需要更新的文件

| 文件 | 更新内容 | 触发时机 |
|------|----------|----------|
| `memory/current-progress.md` | 已完成 / 进行中 / 待开始 的勾选状态 | 每完成一个功能 |
| `spec/XX_xxx.md` | 状态标签（规划中→开发中→已完成） | 功能状态变更时 |
| `spec/XX_xxx.md` | 技术实现要点 checkbox | 每完成一个实现点 |

## 更新格式

### memory/current-progress.md

将已完成项从 `[ ]` 改为 `[x]`，必要时新增条目：

```markdown
## 已完成
- [x] 功能A 已完成
- [x] 新增：功能B

## 进行中
- [ ] 功能C（当前进度描述）

## 待开始
- [ ] 功能D
```

### spec 状态标签

```markdown
> **状态**: 📝 规划中 | 🚧 开发中 | ✅ 已完成
```

## 本次对话已完成项速查

以下为本次对话（首个实现会话）完成的全部内容：

- [x] Rules & Spec 体系建立（CLAUDE.md + 9个rules + spec模板）
- [x] 用户类型定义 `types/user.ts`
- [x] API 服务层 `services/api.ts` + `services/auth.ts`
- [x] 用户 Store `stores/user.ts`（Pinia Setup Store + token持久化）
- [x] 路由守卫 `router/guards.ts` + 路由更新
- [x] 登录页 `LoginView.vue`（表单校验 + loading状态）
- [x] 注册页 `RegisterView.vue`（密码确认校验）
- [x] 首页 `HomeView.vue`（登录/登出状态展示）
- [x] 占位页 `LibraryView.vue` + `ReaderView.vue`
- [x] 前端基础设施：main.ts迁移、@别名、SCSS、Element Plus、Prettier
- [x] 后端认证接口：login、register（含JWT）、profile
- [x] 后端 CORS + 配置模块
- [x] 密码加密从 SHA256 改为明文传输（bcrypt 入库）

**下次对话从此继续。**

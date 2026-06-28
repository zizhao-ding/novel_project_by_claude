# 架构决策记录

> **类型**: 项目架构
> **最后更新**: 2026-06-28
> **关联层级**: Harness Layer 3 — 方案层

## 目的

记录开发过程中的关键架构决策，填补 Layer 3 方案层空缺。每次重大功能实现后应在此补充决策记录。

---

## ADR-001: 权限系统 — 纯可见性控制

**日期**: 2026-06-27
**关联**: REQ-P3-004

### 决策

权限系统采用**单一 visibility 字段**实现内容分发控制，书架不承担权限职责。

### 方案

```
visibility: public    → 所有用户可见（含未登录）
visibility: seed      → 种子成员及以上可见
visibility: admin     → 仅管理员可见
```

- 普通成员可直接阅读所有 `public` 小说，无需加入书架
- 书架回归收藏夹本质
- 一层字段完成内容分发，无复杂权限矩阵

### 替代方案（已否决）

- 书架阅读限制：普通成员只能阅读已加入书架的小说 → **否决**，过于复杂且违背书架作为收藏夹的直觉

### 影响

- 后端：Novel 模型新增 visibility 字段，列表接口自动过滤
- 前端：`usePermission.ts` 提供 `canViewNovel(novel)` 判断
- 路由：`meta.roles` 控制页面级访问

---

## ADR-002: AppHeader — 全局统一顶栏

**日期**: 2026-06-28
**关联**: REQ-P3-002

### 决策

所有页面使用统一的 `AppHeader.vue` 全局顶栏组件，替代各页面自行实现的顶栏。

### 方案

```
┌──────────────────────────────────────────┐
│  ← 返回/标题  │  (搜索)  │  👤 头像悬浮  │
└──────────────────────────────────────────┘
```

- 左侧：返回按钮 + 页面标题，整块可点击（扩大点击区域）
- 中间：搜索入口（可选显示）
- 右侧：用户头像，hover 弹出悬浮卡片（头像/用户名/角色/快捷入口）
- 管理员悬浮卡片额外显示用户管理入口

### 影响

- 统一了 Library/Upload/User/Login/Register 等 8+ 页面的顶栏
- 悬浮卡片提供全局快捷导航（用户页/帮助/用户管理/退出）

---

## ADR-003: 阅读器 — 三主题 + 进度持久化

**日期**: 2026-06-28
**关联**: REQ-P2-002

### 决策

阅读器采用**侧边栏目录 + 正文区 + 底部工具栏**三段布局，支持三种主题和自动进度保存。

### 方案

```
┌── side ──┬── content ────────────┐
│  chapter │  正文区                 │
│  列表    │  (可调字号 12-24px)     │
│          │                        │
├──────────┴────────────────────────┤
│  ← 章  [进度]  主题  字号  → 章   │
└──────────────────────────────────┘
```

- 三种主题：日间（白底黑字）/ 夜间（黑底灰字）/ 护眼（暖黄底棕字）
- 字号调节：12px - 24px 无极调节
- 阅读进度：自动保存到后端 ReadingProgress 模型，重新进入提示恢复
- 章节导航：上一章/下一章按钮 + 侧边栏章节列表

### 技术要点

- 进度保存使用**防抖**避免频繁请求
- 主题/字号偏好存储在 readerStore 中，切换章节保持

---

## ADR-004: 敏感操作二次确认 — 视图层职责

**日期**: 2026-06-26
**关联**: 架构规范 第6节

### 决策

二次确认弹窗（`ElMessageBox.confirm`）在**视图组件**中调用，不在 Store 中调用。

### 理由

- Store 不应依赖 UI 组件（ElMessageBox），保持纯数据逻辑
- 视图层负责用户交互流程，Store 只负责数据操作
- 便于 Store 的单元测试（不依赖 DOM/UI）

### 示例

```typescript
// ✅ 视图层
async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定删除？', '确认', { type: 'warning' });
  await novelStore.removeNovel(id); // Store 只管数据
}

// ❌ Store 中调用 ElMessageBox（违反职责分离）
```

---

## ADR-005: 后端权限依赖 — 函数式依赖注入

**日期**: 2026-06-27
**关联**: REQ-P3-004

### 决策

使用 FastAPI `Depends` 实现函数式权限校验链。

### 方案

```python
# 获取当前用户（解析 JWT）
def get_current_user(...) -> User

# 要求指定角色
def require_role(*roles: str):
    def checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(403)
        return current_user
    return checker

# 要求最低角色
def require_min_role(min_role: str): ...
```

### 影响

- 路由处理函数通过 `Depends(require_role("admin"))` 一行声明权限
- 权限逻辑集中、可组合、可测试

---

## 模板

新建决策时复制此模板：

```markdown
## ADR-xxx: 决策标题

**日期**: YYYY-MM-DD
**关联**: REQ-xxx

### 决策
简述做了什么决定。

### 方案
技术方案要点。

### 替代方案（已否决）
考虑过但未采用的方案及否决原因。

### 影响
该决策对代码库的影响范围。
```

**Why:** Layer 3 方案层需要有架构决策记录，否则每次新会话无法理解过去的设计意图。

**How to apply:** 每次重大功能开发完成后，在此补充对应的 ADR 记录。新会话遇到架构问题时先查看本文。

**相关记忆**: [[03_current-progress]] [[04_harness-architecture]] [[05_testing-debt]]

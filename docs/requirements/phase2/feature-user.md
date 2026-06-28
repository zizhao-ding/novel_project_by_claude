# REQ-P2-003: 用户页面

> **状态**: ✅ done（修改密码功能待补充）
> **优先级**: P1
> **创建日期**: 2026-06-27
> **最后更新**: 2026-06-28

## 1. 概述

实现用户个人页面（UserView.vue），展示用户头像、用户名、角色身份、数据统计和常用功能入口。从书房页面右上角头像点击进入。

## 2. 用户故事

- 作为 **用户**，我想要 **查看我的个人信息**，以便 **了解我的账号状态**
- 作为 **用户**，我想要 **看到我的角色标识**，以便 **确认我的身份权限**
- 作为 **用户**，我想要 **查看阅读统计数据**，以便 **了解我的使用情况**
- 作为 **用户**，我想要 **快速进入常用功能**，以便 **提高操作效率**
- 作为 **用户**，我想要 **修改登录密码**，以便 **保障账号安全**

## 3. UI 布局

```
┌─────────────────────────────────┐
│ ← 我的                          │  ← 顶部栏
├─────────────────────────────────┤
│ ┌─────────────────────────────┐ │
│ │  [头像]  用户名              │ │
│ │          [管理员]            │ │  ← 渐变背景用户卡片
│ │  📅 加入于 2026-06-25       │ │
│ └─────────────────────────────┘ │
├─────────────────────────────────┤
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐   │
│ │ 6  │ │ 6  │ │ 4  │ │8MB │   │  ← 数据统计卡片
│ │书架│ │上传│ │分类│ │空间│   │
│ └────┘ └────┘ └────┘ └────┘   │
├─────────────────────────────────┤
│ 内容管理                        │
│ ┌─────────────────────────────┐ │
│ │ 📚 我的书房              >  │ │
│ │ 📤 上传小说              >  │ │  ← 功能菜单
│ └─────────────────────────────┘ │
│ 账号设置                        │
│ ┌─────────────────────────────┐ │
│ │ 🔒 修改密码              >  │ │
│ │ 🚪 退出登录              >  │ │
│ └─────────────────────────────┘ │
├─────────────────────────────────┤
│     小说阅读平台 v1.0.0         │  ← 版本信息
└─────────────────────────────────┘
```

## 4. 路由 & 页面

- **路由**: `/user`
- **页面**: `UserView.vue`
- **权限**: 需要登录（`meta.requiresAuth: true`）
- **入口**: 书房页面右上角头像点击

## 5. 组件树

```
UserView.vue
├── header               # 顶部导航栏
├── profile-card         # 用户信息卡片（渐变背景）
│   ├── el-avatar        # 头像
│   ├── username         # 用户名
│   ├── el-tag           # 角色标签
│   └── join-date        # 加入日期
├── stats-grid           # 数据统计网格
│   └── stat-card × 4    # 书架/上传/分类/空间
├── menu-group × 2       # 功能菜单组
│   └── menu-item         # 菜单项
└── footer               # 版本信息
```

## 6. 数据流 & Store 设计

使用现有 `useUserStore` 获取用户信息，额外调用统计 API。

```typescript
// 用户角色
type UserRole = 'admin' | 'seed_member' | 'member';

// 角色显示
const ROLE_LABELS = { admin: '管理员', seed_member: '种子成员', member: '普通成员' };
const ROLE_COLORS = { admin: '#e74c3c', seed_member: '#f39c12', member: '#909399' };

// 统计数据
interface UserStats {
  novel_count: number;
  bookshelf_count: number;
  category_count: number;
  total_size: number;
}
```

## 7. API 契约

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/profile` | GET | 获取用户信息（含 role） |
| `/api/auth/user/stats` | GET | 获取用户统计数据 |
| `/api/auth/change-password` | POST | 修改密码（需登录） |

### 修改密码接口
```
POST /api/auth/change-password
Headers: Authorization: Bearer <token>
Body: {
  old_password: string,    // 旧密码
  new_password: string     // 新密码（最少 6 位）
}
Response: { code: 0, message: "密码修改成功" }
```

### 用户模型扩展

```python
# User 模型新增字段
role: str = Field(default="member", max_length=20)
# 可选值: admin / seed_member / member
```

## 8. 验收标准

- [x] 页面顶部显示渐变背景用户卡片
- [x] 显示用户头像（首字母占位）
- [x] 显示用户名
- [x] 显示用户角色标签（管理员/种子成员/普通成员，不同颜色）
- [x] 显示加入日期
- [x] 显示数据统计（书架藏书、上传小说、自建分类、存储空间）
- [x] 统计卡片可点击跳转（书架跳书房）
- [x] 功能菜单分组显示（内容管理、账号设置）
- [x] 菜单项点击跳转对应页面
- [x] 退出登录二次确认
- [x] 底部显示版本信息
- [ ] 修改密码功能可用（需输入旧密码 + 新密码，后端校验后更新）

## 9. 技术实现要点

### 后端
- [x] User 模型新增 `role` 字段
- [x] UserResponse Schema 增加 role
- [x] 新增 `/api/auth/user/stats` 统计接口
- [x] 所有认证响应（register/login/profile）返回 role
- [x] 种子数据脚本设置 test 用户为 admin
- [ ] 新增 `/api/auth/change-password` 接口（校验旧密码 → bcrypt 哈希新密码 → 更新）

### 前端
- [x] User 类型扩展（UserRole、ROLE_LABELS、ROLE_COLORS、UserStats）
- [x] auth API 新增 getUserStats
- [x] UserView.vue 页面实现
- [x] 路由配置 `/user`
- [x] 书房页头像添加 router-link 跳转

## 10. 参考 & 备注

- 参考微信读书、起点读书的个人中心页面
- 角色体系：管理员 > 种子成员 > 普通成员
- 渐变头部使用 Element Plus 主色变量

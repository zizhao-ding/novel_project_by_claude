# 01 — 项目结构 & 文件命名

## 目录结构

```
src/
├── assets/          # 静态资源（图片、图标、字体、全局样式）
├── components/      # 公共组件
│   ├── base/        #   基础组件（Button, Input, Modal 等通用封装）
│   ├── business/    #   业务组件（NovelCard, UploadPanel 等）
│   └── ui/          #   UI 组件（布局、容器等）
├── views/           # 页面视图组件（每个路由对应一个视图）
├── router/          # 路由配置
├── stores/          # Pinia 状态管理
├── services/        # API 服务层（HTTP 请求封装）
├── composables/     # Vue Composables（可复用逻辑）
├── utils/           # 纯工具函数
├── types/           # TypeScript 类型定义
├── directives/      # Vue 自定义指令
├── plugins/         # Vue 插件
└── constants/       # 常量定义
```

## 文件命名规范

| 文件类型 | 命名方式 | 示例 |
|----------|----------|------|
| Vue 组件 | **PascalCase** | `UserCard.vue`, `NovelReader.vue` |
| JS/TS 工具 | **kebab-case** | `api-client.ts`, `format-date.ts` |
| 样式文件 | **kebab-case** | `variables.scss`, `common.scss` |
| 类型定义 | **kebab-case** | `novel.ts`, `user.ts` |
| 测试文件 | `*.spec.ts` | `user-card.spec.ts` |
| Store 文件 | 名词单数 | `user.ts`, `novel.ts`（非 `users.ts`） |
| 视图文件 | 以 `View` 结尾 | `HomeView.vue`, `LibraryView.vue` |

## ✅ 正确 vs ❌ 错误

```typescript
// ✅ 组件导入使用 @ 别名
import UserCard from '@/components/base/UserCard.vue';

// ✅ 工具函数导入
import { formatDate } from '@/utils/format-date';

// ❌ 禁止使用相对路径跨层级导入
import UserCard from '../../../components/UserCard.vue';

// ❌ 禁止组件使用 kebab-case 命名
// ❌ user-card.vue
```

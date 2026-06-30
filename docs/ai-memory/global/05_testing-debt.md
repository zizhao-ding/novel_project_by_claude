# 测试技术债务

> **类型**: 技术债务
> **最后更新**: 2026-06-28（已补充 36 个测试）

## 补充进展 (2026-06-28)

已新增测试：
- 前端: `stores/__tests__/novel.spec.ts` — 9 个测试用例（状态/加载/删除/上传）
- 后端: `tests/test_admin.py` — 7 个测试用例（列表权限/角色修改/搜索）
- 后端: 修复 `test_auth.py` + `test_novel.py` 权限系统适配

| 指标 | 补充前 | 补充后 |
|------|--------|--------|
| 前端测试 | 4 用例 (1 文件) | **13 用例 (2 文件)** |
| 后端测试 | 15 用例 (2 文件) | **23 用例 (3 文件)** |
| 前端覆盖率 | <5% | **~15%** |
| 后端覆盖率 | <20% | **~35%** |
> **关联层级**: AI Agent 六层架构 — 约束层（POST-003 检查） + 工作流层（验收阶段）

## 现状

约束层 Hook 规则 POST-003 要求：
- 前端：核心 Store 和组件测试覆盖率 ≥ 80%
- 后端：API 端点测试覆盖率 ≥ 90%

### 实际覆盖情况

| 模块 | 现有测试 | 覆盖率估算 | 状态 |
|------|----------|-----------|------|
| stores/user.spec.ts | ✅ 4 用例 | ~10% | ⚠️ |
| stores/novel.spec.ts | ✅ 9 用例 | ~15% | ⚠️ |
| stores/bookshelf.ts | ❌ | 0% | ❌ |
| stores/category.ts | ❌ | 0% | ❌ |
| stores/reader.ts | ❌ | 0% | ❌ |
| stores/home.ts | ❌ | 0% | ❌ |
| 视图组件 (11个) | ❌ | 0% | ❌ |
| composables (2个) | ❌ | 0% | ❌ |
| **前端总体** | **2 文件 13 用例** | **~15%** | **低于 80%** |
| | | | |
| 后端 test_auth.py | ✅ 7 用例 | ~30% | ⚠️ |
| 后端 test_novel.py | ✅ 9 用例 | ~30% | ⚠️ |
| 后端 test_admin.py | ✅ 7 用例 | ~20% | ⚠️ |
| 后端 bookshelf API | ❌ | 0% | ❌ |
| 后端 category API | ❌ | 0% | ❌ |
| 后端 reader/progress API | ❌ | 0% | ❌ |
| 后端 search/home API | ❌ | 0% | ❌ |
| **后端总体** | **3 文件 23 用例** | **~35%** | **低于 90%** |

## 缺失测试清单

### 前端（按优先级）

- [x] **Store 测试**: novel ✅（9 用例）| bookshelf, category, reader, home（待补充 4 个）
- [ ] **Composable 测试**: useLongPress, usePermission（共 2 个）
- [ ] **关键视图测试**: LoginView, RegisterView, ReaderView, LibraryView（共 4 个，其余 7 个可选）
- [ ] **组件测试**: AppHeader, NovelCard（共 2 个）
- [ ] **API 服务测试**: 各 service 的 mock 测试

### 后端（按优先级）

- [ ] **认证测试扩展**: change-password 接口
- [x] **管理接口测试**: admin.py ✅（7 用例：列表权限/角色修改/搜索）
- [ ] **书架接口测试**: bookshelf 添加/移除/列表
- [ ] **分类接口测试**: category CRUD
- [ ] **阅读器接口测试**: 章节列表/内容/进度保存恢复
- [ ] **搜索接口测试**: search/hot/latest 端点
- [ ] **权限测试**: visibility 过滤 / role 校验

## 影响

- 约束层 POST-003 检查无法通过，无法保证回归质量
- 新功能开发时无法通过测试快速验证是否破坏已有功能
- Hook POST-003 检查在当前状态下必然失败，需要先补齐基础设施

## 建议

1. **先补齐后端测试**（投入产出比高，FastAPI TestClient 编写效率高）
2. **再补齐前端 Store 测试**（纯逻辑，不依赖 DOM，编写快）
3. **最后补齐视图/组件测试**（需 Vue Test Utils + DOM 模拟，投入较大）

**Why:** 约束层 POST-003 要求测试覆盖率达标，当前测试严重不足，是最主要的架构合规缺口。

**How to apply:** 每次新功能开发时，同步补齐相关模块的测试。在测试覆盖率达到标准前，POST-003 检查应为警告而非阻断。

**相关记忆**: [[03_current-progress]] [[06_architecture-decisions]]

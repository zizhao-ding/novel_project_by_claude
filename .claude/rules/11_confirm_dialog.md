# 11 — 敏感操作二次确认规范

## 核心原则

任何**不可逆或高风险操作**，执行前必须弹出确认对话框，用户确认后才执行。

## 需要二次确认的操作

| 类别 | 操作 |
|------|------|
| 删除 | 删除小说、删除书签、删除账号、删除文件 |
| 退出 | 退出登录 |
| 覆盖 | 覆盖已有文件、替换内容 |
| 发布 | 公开发布内容 |

## 实现方式

统一使用 `ElMessageBox.confirm`：

```typescript
import { ElMessageBox, ElMessage } from 'element-plus';

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm(
      '删除后不可恢复，确定要删除吗？',
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    // 用户确认后执行
    await api.deleteItem(id);
    ElMessage.success('删除成功');
  } catch {
    // 用户取消，不做任何操作
  }
}
```

## 标准模板

```typescript
// ✅ 正确：先确认再执行
async function handleSensitiveAction() {
  try {
    await ElMessageBox.confirm('提示文案', '确认标题', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    // 执行操作...
  } catch {
    // 用户取消
  }
}

// ❌ 错误：直接执行
async function handleDelete(id: number) {
  await api.delete(id); // 没有确认步骤！
}
```

## ❌ 禁止事项

- ❌ 删除操作禁止不弹窗确认直接执行
- ❌ 退出登录禁止不弹窗确认

## ✅ 规则速查

- ✅ 所有删除操作必须用 `ElMessageBox.confirm` 二次确认
- ✅ 退出、覆盖等敏感操作同理
- ✅ 确认文案要明确说明后果（如「不可恢复」）

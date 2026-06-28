<template>
  <div class="admin-users">
    <header class="admin-users__header">
      <div class="admin-users__header-left">
        <router-link to="/" class="admin-users__back">
          <el-icon><ArrowLeft /></el-icon>
        </router-link>
        <h1 class="admin-users__title">用户管理</h1>
      </div>
    </header>

    <div class="admin-users__content">
      <div class="admin-users__search">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索用户名..."
          clearable
          style="max-width: 300px"
          @input="handleSearch"
          @clear="fetchUsers"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <div v-loading="loading" class="admin-users__table-wrap">
        <el-table :data="users" stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" />
          <el-table-column label="角色" width="180">
            <template #default="{ row }">
              <el-select
                :model-value="row.role"
                size="small"
                :disabled="row.id === userStore.user?.id"
                @change="(val: string) => handleRoleChange(row.id, val)"
              >
                <el-option label="管理员" value="admin" />
                <el-option label="种子成员" value="seed_member" />
                <el-option label="普通成员" value="member" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="注册时间" width="220">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button size="small" type="primary" :disabled="row.id === userStore.user?.id" @click="handleRoleChange(row.id, row.role)"
                >保存</el-button
              >
            </template>
          </el-table-column>
        </el-table>

        <div class="admin-users__pagination">
          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="total"
            layout="total, prev, pager, next"
            @current-change="fetchUsers"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ArrowLeft, Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import { useUserStore } from '../stores/user';
import { adminApi } from '../services/admin';

interface AdminUser {
  id: number;
  username: string;
  role: string;
  avatar: string;
  created_at: string;
}

const userStore = useUserStore();
const users = ref<AdminUser[]>([]);
const loading = ref(false);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(20);
const searchKeyword = ref('');

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

async function fetchUsers() {
  loading.value = true;
  try {
    const response = await adminApi.getUsers(currentPage.value, pageSize.value);
    const res = response as unknown as { code: number; data: { users: AdminUser[]; total: number } };
    if (res.code === 0 && res.data) {
      users.value = res.data.users;
      total.value = res.data.total;
    }
  } catch {
    ElMessage.error('获取用户列表失败');
  } finally {
    loading.value = false;
  }
}

async function handleSearch() {
  const kw = searchKeyword.value.trim();
  if (!kw) {
    fetchUsers();
    return;
  }
  loading.value = true;
  try {
    const response = await adminApi.searchUsers(kw);
    const res = response as unknown as { code: number; data: { users: AdminUser[]; total: number } };
    if (res.code === 0 && res.data) {
      users.value = res.data.users;
      total.value = res.data.total;
    }
  } catch {
    ElMessage.error('搜索失败');
  } finally {
    loading.value = false;
  }
}

async function handleRoleChange(userId: number, newRole: string) {
  try {
    const response = await adminApi.updateUserRole(userId, newRole);
    const res = response as unknown as { code: number; message: string };
    if (res.code === 0) {
      ElMessage.success(res.message || '角色修改成功');
      fetchUsers();
    } else {
      ElMessage.error(res.message || '修改失败');
    }
  } catch {
    ElMessage.error('操作失败');
  }
}

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped lang="scss">
.admin-users {
  min-height: 100vh;
  background: var(--el-bg-color-page, #f5f7fa);

  &__header {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    background: #fff;
    border-bottom: 1px solid var(--el-border-color-light);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  &__header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  &__back {
    display: flex;
    align-items: center;
    color: var(--el-text-color-primary);
    font-size: 20px;
    cursor: pointer;
  }

  &__title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
  }

  &__content {
    padding: 24px;
    max-width: 1000px;
  }

  &__search {
    margin-bottom: 16px;
  }

  &__table-wrap {
    background: #fff;
    border-radius: 8px;
    padding: 16px;
  }

  &__pagination {
    margin-top: 16px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>

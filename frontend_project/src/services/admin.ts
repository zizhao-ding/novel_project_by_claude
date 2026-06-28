import { api } from './api';

interface AdminUser {
  id: number;
  username: string;
  role: string;
  avatar: string;
  created_at: string;
}

interface UserListData {
  users: AdminUser[];
  total: number;
}

export const adminApi = {
  /** 获取所有用户列表 */
  getUsers: (page = 1, pageSize = 20) =>
    api.client.get<{ code: number; data: UserListData }>('/admin/users', { params: { page, page_size: pageSize } }),

  /** 修改用户角色 */
  updateUserRole: (userId: number, role: string) =>
    api.client.put<{ code: number; message: string }>(`/admin/users/${userId}/role`, { role }),

  /** 搜索用户 */
  searchUsers: (keyword: string) => api.client.get<{ code: number; data: UserListData }>('/admin/users/search', { params: { keyword } }),
};

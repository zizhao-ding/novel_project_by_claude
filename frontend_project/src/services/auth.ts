import { api } from './api';
import type { ApiResponse, User, UserStats, RegisterRequest, LoginRequest, LoginResponse } from '../types/user';

export const authApi = {
  /** 用户注册 */
  register: (data: RegisterRequest & { avatar?: string }) => api.client.post<ApiResponse<User>>('/auth/register', data),

  /** 用户登录 */
  login: (data: LoginRequest) => api.client.post<ApiResponse<LoginResponse>>('/auth/login', data),

  /** 获取当前用户信息 */
  getProfile: () => api.client.get<ApiResponse<User>>('/auth/profile'),

  /** 获取用户统计数据 */
  getUserStats: () => api.client.get<{ code: number; data: UserStats }>('/auth/user/stats'),

  /** 修改密码 */
  changePassword: (oldPassword: string, newPassword: string) =>
    api.client.post<{ code: number; message: string }>('/auth/change-password', {
      old_password: oldPassword,
      new_password: newPassword,
    }),
};

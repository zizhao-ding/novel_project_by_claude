import { api } from './api';
import type { ApiResponse, User, RegisterRequest, LoginRequest, LoginResponse } from '../types/user';

export const authApi = {
  /**
   * 用户注册
   * 后端已实现：POST /api/auth/register
   */
  register: (data: RegisterRequest) => api.client.post<ApiResponse<User>>('/auth/register', data),

  /**
   * 用户登录
   * 后端待实现：POST /api/auth/login
   */
  login: (data: LoginRequest) => api.client.post<ApiResponse<LoginResponse>>('/auth/login', data),

  /**
   * 获取当前用户信息
   * 后端待实现：GET /api/auth/profile
   */
  getProfile: () => api.client.get<ApiResponse<User>>('/auth/profile'),
};

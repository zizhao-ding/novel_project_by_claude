// 用户角色
export type UserRole = 'admin' | 'seed_member' | 'member';

// 角色显示名称
export const ROLE_LABELS: Record<UserRole, string> = {
  admin: '管理员',
  seed_member: '种子成员',
  member: '普通成员',
};

// 角色颜色
export const ROLE_COLORS: Record<UserRole, string> = {
  admin: '#e74c3c',
  seed_member: '#f39c12',
  member: '#909399',
};

// 用户信息
export interface User {
  id: number;
  username: string;
  role: UserRole;
  avatar: string;
  created_at: string;
}

// 预设头像颜色
export const AVATAR_PRESETS = ['#F5A623', '#F78DA7', '#8BD3DD', '#A8D8B9', '#FF6B6B', '#C9B1FF', '#FFD93D', '#6BCB77'];

// 用户统计数据
export interface UserStats {
  novel_count: number;
  bookshelf_count: number;
  category_count: number;
  total_size: number;
}

// 后端统一响应格式
export interface ApiResponse<T = unknown> {
  code: number; // 0 = 成功, 非0 = 失败
  message: string;
  data: T | null;
}

// 注册请求
export interface RegisterRequest {
  username: string;
  password: string;
}

// 登录请求
export interface LoginRequest {
  username: string;
  password: string;
}

// 登录响应（预期后端实现后的格式）
export interface LoginResponse {
  token: string;
  user: User;
}

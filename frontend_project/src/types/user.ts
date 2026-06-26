// 用户信息
export interface User {
  id: number;
  username: string;
  created_at: string;
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

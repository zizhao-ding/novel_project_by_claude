import axios from 'axios';
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { ElMessage } from 'element-plus';

class ApiService {
  private instance: AxiosInstance;

  constructor() {
    this.instance = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' },
    });
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截：自动附加 Token
    this.instance.interceptors.request.use((config: InternalAxiosRequestConfig) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // 响应拦截：统一错误处理
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => response.data,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          ElMessage.error('登录已过期，请重新登录');
        } else if (error.response?.status >= 500) {
          ElMessage.error('服务器错误，请稍后重试');
        }
        return Promise.reject(error);
      },
    );
  }

  get client() {
    return this.instance;
  }
}

export const api = new ApiService();

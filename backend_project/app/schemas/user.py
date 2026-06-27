from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserRegisterRequest(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=100, description="账号")
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    avatar: str = Field(default="#F5A623", max_length=200, description="头像颜色值")


class UserLoginRequest(BaseModel):
    """用户登录请求"""
    username: str = Field(..., min_length=1, max_length=100, description="账号")
    password: str = Field(..., min_length=1, max_length=128, description="密码")


class UserResponse(BaseModel):
    """用户信息"""
    id: int
    username: str
    role: str = "member"
    avatar: str = "#F5A623"
    created_at: datetime

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    """登录响应数据"""
    token: str
    user: UserResponse


class AuthResponse(BaseModel):
    """注册/资料 通用响应"""
    code: int = Field(default=0, description="状态码")
    message: str = Field(default="", description="提示信息")
    data: Optional[UserResponse] = Field(default=None)


class LoginResponse(BaseModel):
    """登录响应"""
    code: int = Field(default=0, description="状态码")
    message: str = Field(default="", description="提示信息")
    data: Optional[LoginData] = Field(default=None)


class UserStatsData(BaseModel):
    """用户统计数据"""
    novel_count: int = 0
    bookshelf_count: int = 0
    category_count: int = 0
    total_size: int = 0


class UserStatsResponse(BaseModel):
    """用户统计响应"""
    code: int = 0
    message: str = ""
    data: Optional[UserStatsData] = None

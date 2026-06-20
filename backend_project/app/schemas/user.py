from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserRegisterRequest(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=100, description="账号")
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class UserResponse(BaseModel):
    """用户信息"""
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    """用户注册响应"""
    code: int = Field(description="状态码, 0表示成功")
    message: str = Field(description="提示信息")
    data: Optional[UserResponse] = Field(default=None, description="用户信息")

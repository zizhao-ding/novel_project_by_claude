from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """用户模型"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True, index=True, description="用户名/账号")
    password: str = Field(default="", max_length=128, description="明文密码")
    password_hash: str = Field(max_length=255, description="密码哈希")
    role: str = Field(default="member", max_length=20, description="用户角色: admin / seed_member / member")
    avatar: str = Field(default="#F5A623", max_length=200, description="头像（颜色值或图片URL）")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

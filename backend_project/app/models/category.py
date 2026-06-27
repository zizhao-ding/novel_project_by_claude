from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Category(SQLModel, table=True):
    """分类模型"""
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, description="所属用户ID")
    name: str = Field(max_length=50, description="分类名称")
    color: str = Field(max_length=20, default="#409eff", description="分类颜色")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")

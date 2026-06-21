from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Novel(SQLModel, table=True):
    """小说模型"""
    __tablename__ = "novels"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, description="上传用户ID")
    title: str = Field(max_length=255, description="小说标题")
    file_path: str = Field(max_length=500, description="文件存储路径")
    file_size: int = Field(default=0, description="文件大小（字节）")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="上传时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

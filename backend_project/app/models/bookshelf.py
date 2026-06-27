from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Bookshelf(SQLModel, table=True):
    """书架模型 — 记录用户将哪些小说加入书架"""
    __tablename__ = "bookshelves"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, description="用户ID")
    novel_id: int = Field(foreign_key="novels.id", index=True, description="小说ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="加入书架时间")

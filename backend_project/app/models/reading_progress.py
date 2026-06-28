from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ReadingProgress(SQLModel, table=True):
    """阅读进度模型"""
    __tablename__ = "reading_progress"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, description="用户ID")
    novel_id: int = Field(foreign_key="novels.id", index=True, description="小说ID")
    chapter_index: int = Field(default=0, description="当前阅读章节索引")
    scroll_percent: float = Field(default=0, description="滚动百分比 0-100")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

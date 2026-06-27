from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class BookshelfNovel(BaseModel):
    """书架中的小说信息（含分类）"""
    id: int
    novel_id: int
    title: str
    file_size: int
    category_id: Optional[int] = None
    added_at: datetime

    class Config:
        from_attributes = True


class BookshelfListData(BaseModel):
    """书架列表数据"""
    items: List[BookshelfNovel]
    total: int


class BookshelfListResponse(BaseModel):
    """书架列表响应"""
    code: int = 0
    message: str = ""
    data: Optional[BookshelfListData] = None


class BookshelfApiResponse(BaseModel):
    """书架操作响应"""
    code: int = 0
    message: str = ""
    data: Optional[dict] = None


class AddToBookshelfRequest(BaseModel):
    """加入书架请求"""
    novel_id: int

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NovelResponse(BaseModel):
    """小说信息"""
    id: int
    user_id: int
    title: str
    file_size: int
    created_at: datetime

    class Config:
        from_attributes = True


class NovelListData(BaseModel):
    """小说列表数据"""
    items: List[NovelResponse]
    total: int


class NovelApiResponse(BaseModel):
    """小说通用响应"""
    code: int = 0
    message: str = ""
    data: Optional[NovelResponse] = None


class NovelListResponse(BaseModel):
    """小说列表响应"""
    code: int = 0
    message: str = ""
    data: Optional[NovelListData] = None

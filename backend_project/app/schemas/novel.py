from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NovelResponse(BaseModel):
    """小说信息"""
    id: int
    user_id: int
    title: str
    file_size: int
    category_id: Optional[int] = None
    visibility: str = "public"
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


class HotNovelItem(BaseModel):
    """热门推荐小说项"""
    id: int
    user_id: int
    title: str
    file_size: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    visibility: str = "public"
    bookshelf_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class HotNovelListData(BaseModel):
    items: List[HotNovelItem]
    total: int


class HotNovelListResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[HotNovelListData] = None


class ChapterInfo(BaseModel):
    """章节信息"""
    index: int
    title: str
    start_pos: int
    length: int


class ChapterListData(BaseModel):
    """章节目录数据"""
    novel_id: int
    chapters: List[ChapterInfo]


class ChapterListResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[ChapterListData] = None


class ChapterContent(BaseModel):
    """章节正文"""
    index: int
    title: str
    content: str
    prev_index: Optional[int] = None
    next_index: Optional[int] = None


class ChapterContentResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[ChapterContent] = None


class ReadingProgressData(BaseModel):
    """阅读进度"""
    chapter_index: int
    scroll_percent: float = 0
    updated_at: datetime


class ReadingProgressResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[ReadingProgressData] = None


class SaveProgressRequest(BaseModel):
    """保存进度请求"""
    chapter_index: int
    scroll_percent: float = Field(default=0, ge=0, le=100)


class SearchResultItem(BaseModel):
    """搜索结果项"""
    id: int
    user_id: int
    title: str
    file_size: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    visibility: str = "public"
    created_at: datetime

    class Config:
        from_attributes = True


class SearchResultData(BaseModel):
    items: List[SearchResultItem]
    total: int
    page: int
    page_size: int


class SearchResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[SearchResultData] = None


class VisibilityUpdateRequest(BaseModel):
    """小说可见性修改请求"""
    visibility: str = Field(..., description="public / seed / admin")

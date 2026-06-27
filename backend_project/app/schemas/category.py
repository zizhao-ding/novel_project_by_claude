from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CategoryCreate(BaseModel):
    """创建分类请求"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名称")
    color: str = Field(default="#409eff", max_length=20, description="分类颜色")


class CategoryUpdate(BaseModel):
    """更新分类请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="分类名称")
    color: Optional[str] = Field(None, max_length=20, description="分类颜色")


class CategoryResponse(BaseModel):
    """分类信息"""
    id: int
    user_id: int
    name: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryListData(BaseModel):
    """分类列表数据"""
    items: List[CategoryResponse]
    total: int


class CategoryApiResponse(BaseModel):
    """分类通用响应"""
    code: int = 0
    message: str = ""
    data: Optional[CategoryResponse] = None


class CategoryListResponse(BaseModel):
    """分类列表响应"""
    code: int = 0
    message: str = ""
    data: Optional[CategoryListData] = None


class BatchCategoryRequest(BaseModel):
    """批量修改分类请求"""
    novel_ids: List[int] = Field(..., description="小说ID列表")
    category_id: Optional[int] = Field(None, description="分类ID，null 表示取消分类")


class BatchApiResponse(BaseModel):
    """批量操作响应"""
    code: int = 0
    message: str = ""
    data: Optional[dict] = None

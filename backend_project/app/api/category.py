from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.category import Category
from app.models.novel import Novel
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    CategoryListData,
    CategoryApiResponse,
    CategoryListResponse,
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/api", tags=["分类"])


@router.get("/categories", response_model=CategoryListResponse, summary="分类列表")
def list_categories(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取当前用户的所有分类"""
    categories = session.exec(
        select(Category)
        .where(Category.user_id == current_user.id)
        .order_by(Category.created_at.asc())
    ).all()

    items = [
        CategoryResponse(
            id=c.id,
            user_id=c.user_id,
            name=c.name,
            color=c.color,
            created_at=c.created_at,
        )
        for c in categories
    ]

    return CategoryListResponse(
        code=0, message="获取成功", data=CategoryListData(items=items, total=len(items))
    )


@router.post("/categories", response_model=CategoryApiResponse, summary="创建分类")
def create_category(
    request: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """创建新分类"""
    # 检查同名分类
    existing = session.exec(
        select(Category).where(
            Category.user_id == current_user.id,
            Category.name == request.name,
        )
    ).first()
    if existing:
        return CategoryApiResponse(code=400, message="该分类已存在", data=None)

    category = Category(
        user_id=current_user.id,
        name=request.name,
        color=request.color,
    )
    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryApiResponse(
        code=0,
        message="创建成功",
        data=CategoryResponse(
            id=category.id,
            user_id=category.user_id,
            name=category.name,
            color=category.color,
            created_at=category.created_at,
        ),
    )


@router.put("/categories/{category_id}", response_model=CategoryApiResponse, summary="更新分类")
def update_category(
    category_id: int,
    request: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """更新分类信息"""
    category = session.get(Category, category_id)
    if not category:
        return CategoryApiResponse(code=404, message="分类不存在", data=None)
    if category.user_id != current_user.id:
        return CategoryApiResponse(code=403, message="无权操作", data=None)

    if request.name is not None:
        category.name = request.name
    if request.color is not None:
        category.color = request.color

    session.add(category)
    session.commit()
    session.refresh(category)

    return CategoryApiResponse(
        code=0,
        message="更新成功",
        data=CategoryResponse(
            id=category.id,
            user_id=category.user_id,
            name=category.name,
            color=category.color,
            created_at=category.created_at,
        ),
    )


@router.delete("/categories/{category_id}", response_model=CategoryApiResponse, summary="删除分类")
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """删除分类（会将该分类下的小说设为未分类）"""
    category = session.get(Category, category_id)
    if not category:
        return CategoryApiResponse(code=404, message="分类不存在", data=None)
    if category.user_id != current_user.id:
        return CategoryApiResponse(code=403, message="无权操作", data=None)

    # 将该分类下的小说设为未分类
    novels = session.exec(
        select(Novel).where(Novel.category_id == category_id)
    ).all()
    for novel in novels:
        novel.category_id = None
        session.add(novel)

    session.delete(category)
    session.commit()

    return CategoryApiResponse(code=0, message="删除成功", data=None)

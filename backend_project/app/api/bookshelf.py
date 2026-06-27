from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.bookshelf import Bookshelf
from app.models.novel import Novel
from app.models.user import User
from app.schemas.bookshelf import (
    BookshelfNovel,
    BookshelfListData,
    BookshelfListResponse,
    BookshelfApiResponse,
    AddToBookshelfRequest,
)
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/bookshelf", tags=["书架"])


@router.get("", response_model=BookshelfListResponse, summary="书架列表")
def list_bookshelf(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取当前用户的书架列表（含小说详情）"""
    # 联表查询：bookshelf + novel
    results = session.exec(
        select(Bookshelf, Novel)
        .join(Novel, Bookshelf.novel_id == Novel.id)
        .where(Bookshelf.user_id == current_user.id)
        .order_by(Bookshelf.created_at.desc())
    ).all()

    items = [
        BookshelfNovel(
            id=shelf.id,
            novel_id=novel.id,
            title=novel.title,
            file_size=novel.file_size,
            category_id=novel.category_id,
            added_at=shelf.created_at,
        )
        for shelf, novel in results
    ]

    return BookshelfListResponse(
        code=0, message="获取成功", data=BookshelfListData(items=items, total=len(items))
    )


@router.post("", response_model=BookshelfApiResponse, summary="加入书架")
def add_to_bookshelf(
    request: AddToBookshelfRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """将小说加入书架"""
    # 检查小说是否存在
    novel = session.get(Novel, request.novel_id)
    if not novel:
        return BookshelfApiResponse(code=404, message="小说不存在")

    # 检查是否已在书架中
    existing = session.exec(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.novel_id == request.novel_id,
        )
    ).first()
    if existing:
        return BookshelfApiResponse(code=400, message="已在书架中")

    shelf = Bookshelf(user_id=current_user.id, novel_id=request.novel_id)
    session.add(shelf)
    session.commit()

    return BookshelfApiResponse(code=0, message="已加入书架")


@router.delete("/{novel_id}", response_model=BookshelfApiResponse, summary="从书架移除")
def remove_from_bookshelf(
    novel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """将小说从书架移除"""
    shelf = session.exec(
        select(Bookshelf).where(
            Bookshelf.user_id == current_user.id,
            Bookshelf.novel_id == novel_id,
        )
    ).first()
    if not shelf:
        return BookshelfApiResponse(code=404, message="书架记录不存在")

    session.delete(shelf)
    session.commit()

    return BookshelfApiResponse(code=0, message="已从书架移除")


@router.delete("", response_model=BookshelfApiResponse, summary="批量从书架移除")
def batch_remove_from_bookshelf(
    novel_ids: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """批量从书架移除（novel_ids 逗号分隔）"""
    ids = [int(x.strip()) for x in novel_ids.split(",") if x.strip().isdigit()]
    if not ids:
        return BookshelfApiResponse(code=400, message="请提供要移除的小说ID")

    removed = 0
    for nid in ids:
        shelf = session.exec(
            select(Bookshelf).where(
                Bookshelf.user_id == current_user.id,
                Bookshelf.novel_id == nid,
            )
        ).first()
        if shelf:
            session.delete(shelf)
            removed += 1

    session.commit()
    return BookshelfApiResponse(code=0, message=f"已移除 {removed} 本书籍")

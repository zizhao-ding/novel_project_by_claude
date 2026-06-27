import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select

from app.database import get_session
from app.models.novel import Novel
from app.models.category import Category
from app.models.user import User
from app.schemas.novel import (
    NovelResponse,
    NovelListData,
    NovelApiResponse,
    NovelListResponse,
)
from app.schemas.category import BatchCategoryRequest, BatchApiResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/api", tags=["小说"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "novels")

ALLOWED_EXTENSIONS = {".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def _save_file(user_id: int, file: UploadFile) -> str:
    """保存文件到本地，返回相对路径"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())
    rel_path = f"uploads/novels/{user_id}_{timestamp}_{file.filename}"
    abs_path = os.path.join(UPLOAD_DIR, f"{user_id}_{timestamp}_{file.filename}")
    with open(abs_path, "wb") as f:
        f.write(file.file.read())
    return rel_path


@router.post("/upload/novel", response_model=NovelApiResponse, summary="上传小说")
def upload_novel(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """上传 TXT 小说文件"""

    # 校验扩展名
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return NovelApiResponse(code=400, message="仅支持 TXT 格式", data=None)

    # 校验大小（读内容后检查）
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        return NovelApiResponse(code=400, message="文件大小不能超过 10MB", data=None)

    # 保存文件
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())
    filename = f"{current_user.id}_{timestamp}_{file.filename}"
    abs_path = os.path.join(UPLOAD_DIR, filename)
    with open(abs_path, "wb") as f:
        f.write(content)

    # 提取标题（去掉扩展名）
    title = os.path.splitext(file.filename or "unknown")[0]

    # 写入数据库
    novel = Novel(
        user_id=current_user.id,
        title=title,
        file_path=abs_path,
        file_size=len(content),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(novel)
    session.commit()
    session.refresh(novel)

    return NovelApiResponse(
        code=0,
        message="上传成功",
        data=NovelResponse(
            id=novel.id,
            user_id=novel.user_id,
            title=novel.title,
            file_size=novel.file_size,
            category_id=novel.category_id,
            created_at=novel.created_at,
        ),
    )


@router.get("/novels", response_model=NovelListResponse, summary="小说列表")
def list_novels(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取当前用户的小说列表"""
    offset = (page - 1) * page_size
    novels = session.exec(
        select(Novel).where(Novel.user_id == current_user.id).order_by(Novel.created_at.desc()).offset(offset).limit(page_size)
    ).all()
    total = session.query(Novel).where(Novel.user_id == current_user.id).count()

    items = [
        NovelResponse(
            id=n.id,
            user_id=n.user_id,
            title=n.title,
            file_size=n.file_size,
            category_id=n.category_id,
            created_at=n.created_at,
        )
        for n in novels
    ]

    return NovelListResponse(code=0, message="获取成功", data=NovelListData(items=items, total=total))


@router.put("/novels/batch-category", response_model=BatchApiResponse, summary="批量修改分类")
def batch_update_category(
    request: BatchCategoryRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """批量修改小说的分类"""
    if not request.novel_ids:
        return BatchApiResponse(code=400, message="请选择要操作的小说")

    # 验证分类存在（如果指定了分类）
    if request.category_id is not None:
        category = session.get(Category, request.category_id)
        if not category or category.user_id != current_user.id:
            return BatchApiResponse(code=400, message="分类不存在")

    # 批量更新
    updated = 0
    for novel_id in request.novel_ids:
        novel = session.get(Novel, novel_id)
        if novel and novel.user_id == current_user.id:
            novel.category_id = request.category_id
            session.add(novel)
            updated += 1

    session.commit()

    return BatchApiResponse(code=0, message=f"已更新 {updated} 本书籍", data={"updated": updated})


@router.delete("/novels/{novel_id}", response_model=NovelApiResponse, summary="删除小说")
def delete_novel(
    novel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """删除小说（文件 + 数据库记录）"""
    novel = session.get(Novel, novel_id)
    if not novel:
        return NovelApiResponse(code=404, message="小说不存在", data=None)
    if novel.user_id != current_user.id:
        return NovelApiResponse(code=403, message="无权删除", data=None)

    # 删除文件
    if os.path.exists(novel.file_path):
        os.remove(novel.file_path)

    session.delete(novel)
    session.commit()

    return NovelApiResponse(code=0, message="删除成功", data=None)

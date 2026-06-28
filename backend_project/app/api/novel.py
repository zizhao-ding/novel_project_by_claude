import os
from datetime import datetime  # noqa: F811
from typing import Optional  # noqa: F811

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select, func

from app.database import get_session
from app.models.novel import Novel
from app.models.category import Category
from app.models.user import User
from app.schemas.novel import (
    NovelResponse,
    NovelListData,
    NovelApiResponse,
    NovelListResponse,
    HotNovelItem,
    HotNovelListData,
    HotNovelListResponse,
    ChapterInfo,
    ChapterListData,
    ChapterListResponse,
    ChapterContent,
    ChapterContentResponse,
    ReadingProgressData,
    ReadingProgressResponse,
    SaveProgressRequest,
    SearchResultItem,
    SearchResultData,
    SearchResponse,
    VisibilityUpdateRequest,
)
from app.schemas.category import BatchCategoryRequest, BatchApiResponse
from app.api.auth import get_current_user, require_min_role, require_role

router = APIRouter(prefix="/api", tags=["小说"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "novels")

ALLOWED_EXTENSIONS = {".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# 章节标题正则: 第X章/节/卷
import re

CHAPTER_PATTERN = re.compile(r"^(第[零一二三四五六七八九十百千0-9]+[章节卷集])", re.MULTILINE)


def _get_visible_query(current_user: User):
    """根据用户角色返回可见性过滤条件"""
    if current_user.role == "admin":
        return True
    elif current_user.role == "seed_member":
        return Novel.visibility.in_(["public", "seed"])
    else:
        return Novel.visibility == "public"


def _novel_to_response(n: Novel) -> NovelResponse:
    return NovelResponse(
        id=n.id,
        user_id=n.user_id,
        title=n.title,
        file_size=n.file_size,
        category_id=n.category_id,
        visibility=n.visibility,
        created_at=n.created_at,
    )


def _parse_chapters(file_path: str) -> list[dict]:
    """解析 TXT 文件章节，返回 [{index, title, start_pos, length}]"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    matches = list(CHAPTER_PATTERN.finditer(text))
    if not matches:
        return [{"index": 0, "title": "全文", "start_pos": 0, "length": len(text.encode("utf-8"))}]
    chapters = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = m.group(1).strip()
        chapters.append({"index": i, "title": title, "start_pos": start, "length": end - start})
    return chapters


# ── 上传 ──

@router.post("/upload/novel", response_model=NovelApiResponse, summary="上传小说")
def upload_novel(
    file: UploadFile = File(...),
    visibility: str = "public",
    current_user: User = Depends(require_min_role("seed_member")),
    session: Session = Depends(get_session),
):
    """上传 TXT 小说文件（需种子成员及以上权限）"""
    if visibility not in ("public", "seed", "admin"):
        return NovelApiResponse(code=400, message="无效的可见性值", data=None)

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return NovelApiResponse(code=400, message="仅支持 TXT 格式", data=None)

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        return NovelApiResponse(code=400, message="文件大小不能超过 10MB", data=None)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())
    filename = f"{current_user.id}_{timestamp}_{file.filename}"
    abs_path = os.path.join(UPLOAD_DIR, filename)
    with open(abs_path, "wb") as f:
        f.write(content)

    title = os.path.splitext(file.filename or "unknown")[0]
    novel = Novel(
        user_id=current_user.id,
        title=title,
        file_path=abs_path,
        file_size=len(content),
        visibility=visibility,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(novel)
    session.commit()
    session.refresh(novel)

    return NovelApiResponse(code=0, message="上传成功", data=_novel_to_response(novel))


# ── 列表 ──

@router.get("/novels", response_model=NovelListResponse, summary="小说列表")
def list_novels(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort: str = Query(default="default"),
    category_id: Optional[int] = Query(default=None),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取小说列表（按可见性过滤）"""
    base = select(Novel).where(_get_visible_query(current_user))
    if category_id is not None:
        base = base.where(Novel.category_id == category_id)
    if sort == "hot":
        # 按书架数排序: 左连接 bookshelf, group by novel_id, count
        from app.models.bookshelf import Bookshelf
        base = (
            select(Novel)
            .join(Bookshelf, Novel.id == Bookshelf.novel_id, isouter=True)
            .where(_get_visible_query(current_user))
            .group_by(Novel.id)
            .order_by(func.count(Bookshelf.id).desc())
        )
    elif sort == "latest":
        base = base.order_by(Novel.created_at.desc())
    else:
        base = base.order_by(Novel.created_at.desc())

    offset = (page - 1) * page_size
    novels = session.exec(base.offset(offset).limit(page_size)).all()
    total_count = session.exec(select(func.count()).select_from(Novel).where(_get_visible_query(current_user))).one()

    return NovelListResponse(code=0, message="获取成功", data=NovelListData(items=[_novel_to_response(n) for n in novels], total=total_count))


# ── 热门 ──

@router.get("/novels/hot", response_model=HotNovelListResponse, summary="热门推荐")
def hot_novels(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """热门推荐：按加入书架数降序"""
    from app.models.bookshelf import Bookshelf
    result = session.exec(
        select(
            Novel.id,
            Novel.user_id,
            Novel.title,
            Novel.file_size,
            Novel.category_id,
            Category.name.label("category_name"),
            Novel.visibility,
            Novel.created_at,
            func.count(Bookshelf.id).label("bookshelf_count"),
        )
        .join(Category, Novel.category_id == Category.id, isouter=True)
        .join(Bookshelf, Novel.id == Bookshelf.novel_id, isouter=True)
        .where(_get_visible_query(current_user))
        .group_by(Novel.id)
        .order_by(func.count(Bookshelf.id).desc())
        .limit(limit)
    ).all()
    items = [
        HotNovelItem(
            id=r[0], user_id=r[1], title=r[2], file_size=r[3], category_id=r[4],
            category_name=r[5], visibility=r[6], created_at=r[7], bookshelf_count=r[8],
        )
        for r in result
    ]
    return HotNovelListResponse(code=0, message="获取成功", data=HotNovelListData(items=items, total=len(items)))


# ── 最新 ──

@router.get("/novels/latest", response_model=NovelListResponse, summary="最新上传")
def latest_novels(
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """最新上传：按创建时间降序"""
    novels = session.exec(
        select(Novel).where(_get_visible_query(current_user)).order_by(Novel.created_at.desc()).offset(offset).limit(limit)
    ).all()
    return NovelListResponse(code=0, message="获取成功", data=NovelListData(items=[_novel_to_response(n) for n in novels], total=len(novels)))


# ── 搜索 ──

@router.get("/novels/search", response_model=SearchResponse, summary="搜索小说")
def search_novels(
    keyword: str = Query(default="", min_length=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """按标题搜索小说（按可见性过滤）"""
    from app.models.category import Category
    base = select(Novel).where(_get_visible_query(current_user), Novel.title.contains(keyword))
    total = session.exec(select(func.count()).select_from(Novel).where(_get_visible_query(current_user), Novel.title.contains(keyword))).one()
    novels = session.exec(base.order_by(Novel.created_at.desc()).offset((page - 1) * page_size).limit(page_size)).all()
    items = []
    for n in novels:
        cat = session.get(Category, n.category_id) if n.category_id else None
        items.append(SearchResultItem(
            id=n.id, user_id=n.user_id, title=n.title, file_size=n.file_size,
            category_id=n.category_id, category_name=cat.name if cat else None,
            visibility=n.visibility, created_at=n.created_at,
        ))
    return SearchResponse(code=0, message="搜索完成", data=SearchResultData(items=items, total=total, page=page, page_size=page_size))


# ── 下载 ──

@router.get("/novels/{novel_id}/download", summary="下载小说")
def download_novel(
    novel_id: int,
    current_user: User = Depends(require_min_role("seed_member")),
    session: Session = Depends(get_session),
):
    """下载 TXT 原文件（需种子成员及以上权限）"""
    novel = session.get(Novel, novel_id)
    if not novel:
        raise HTTPException(status_code=404, detail="小说不存在")
    if not os.path.exists(novel.file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(novel.file_path, filename=f"{novel.title}.txt", media_type="text/plain")


# ── 可见性 ──

@router.put("/novels/{novel_id}/visibility", summary="修改可见性")
def update_visibility(
    novel_id: int,
    request: VisibilityUpdateRequest,
    current_user: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """管理员修改小说可见性"""
    if request.visibility not in ("public", "seed", "admin"):
        return {"code": 400, "message": "无效的可见性值"}
    novel = session.get(Novel, novel_id)
    if not novel:
        return {"code": 404, "message": "小说不存在"}
    novel.visibility = request.visibility
    session.add(novel)
    session.commit()
    return {"code": 0, "message": "可见性修改成功"}


# ── 章节 ──

@router.get("/novels/{novel_id}/chapters", response_model=ChapterListResponse, summary="章节目录")
def get_chapters(
    novel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取小说章节目录（按可见性校验）"""
    novel = session.get(Novel, novel_id)
    if not novel:
        return ChapterListResponse(code=404, message="小说不存在", data=None)
    # 可见性校验
    visible = False
    if current_user.role == "admin":
        visible = True
    elif current_user.role == "seed_member":
        visible = novel.visibility in ("public", "seed")
    else:
        visible = novel.visibility == "public"
    if not visible:
        return ChapterListResponse(code=403, message="无权访问", data=None)

    chapters = _parse_chapters(novel.file_path)
    return ChapterListResponse(code=0, message="获取成功", data=ChapterListData(novel_id=novel_id, chapters=[ChapterInfo(**c) for c in chapters]))


@router.get("/novels/{novel_id}/chapters/{index}", response_model=ChapterContentResponse, summary="章节正文")
def get_chapter_content(
    novel_id: int,
    index: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取指定章节的正文内容"""
    novel = session.get(Novel, novel_id)
    if not novel:
        return ChapterContentResponse(code=404, message="小说不存在", data=None)
    visible = False
    if current_user.role == "admin":
        visible = True
    elif current_user.role == "seed_member":
        visible = novel.visibility in ("public", "seed")
    else:
        visible = novel.visibility == "public"
    if not visible:
        return ChapterContentResponse(code=403, message="无权访问", data=None)

    chapters = _parse_chapters(novel.file_path)
    if index < 0 or index >= len(chapters):
        return ChapterContentResponse(code=404, message="章节不存在", data=None)
    c = chapters[index]
    with open(novel.file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(c["start_pos"])
        content = f.read(c["length"])
    return ChapterContentResponse(
        code=0,
        message="获取成功",
        data=ChapterContent(
            index=c["index"],
            title=c["title"],
            content=content,
            prev_index=index - 1 if index > 0 else None,
            next_index=index + 1 if index < len(chapters) - 1 else None,
        ),
    )


# ── 阅读进度 ──

from app.models.reading_progress import ReadingProgress as RPModel


@router.get("/novels/{novel_id}/progress", response_model=ReadingProgressResponse, summary="获取阅读进度")
def get_progress(
    novel_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取当前用户对指定小说的阅读进度"""
    rp = session.exec(select(RPModel).where(RPModel.user_id == current_user.id, RPModel.novel_id == novel_id)).first()
    if rp is None:
        return ReadingProgressResponse(code=0, message="无历史进度", data=None)
    return ReadingProgressResponse(code=0, message="获取成功", data=ReadingProgressData(chapter_index=rp.chapter_index, scroll_percent=rp.scroll_percent, updated_at=rp.updated_at))


@router.post("/novels/{novel_id}/progress", response_model=dict, summary="保存阅读进度")
def save_progress(
    novel_id: int,
    request: SaveProgressRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """保存当前用户对指定小说的阅读进度（upsert）"""
    novel = session.get(Novel, novel_id)
    if not novel:
        return {"code": 404, "message": "小说不存在"}
    rp = session.exec(select(RPModel).where(RPModel.user_id == current_user.id, RPModel.novel_id == novel_id)).first()
    if rp:
        rp.chapter_index = request.chapter_index
        rp.scroll_percent = request.scroll_percent
        rp.updated_at = datetime.utcnow()
    else:
        rp = RPModel(user_id=current_user.id, novel_id=novel_id, chapter_index=request.chapter_index, scroll_percent=request.scroll_percent, updated_at=datetime.utcnow())
    session.add(rp)
    session.commit()
    return {"code": 0, "message": "进度已保存"}


# ── 批量分类 ──

@router.put("/novels/batch-category", response_model=BatchApiResponse, summary="批量修改分类")
def batch_update_category(
    request: BatchCategoryRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """批量修改小说的分类"""
    if not request.novel_ids:
        return BatchApiResponse(code=400, message="请选择要操作的小说")
    if request.category_id is not None:
        category = session.get(Category, request.category_id)
        if not category or category.user_id != current_user.id:
            return BatchApiResponse(code=400, message="分类不存在")
    updated = 0
    for novel_id in request.novel_ids:
        novel = session.get(Novel, novel_id)
        if novel and novel.user_id == current_user.id:
            novel.category_id = request.category_id
            session.add(novel)
            updated += 1
    session.commit()
    return BatchApiResponse(code=0, message=f"已更新 {updated} 本书籍", data={"updated": updated})


# ── 删除 ──

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
    if novel.user_id != current_user.id and current_user.role != "admin":
        return NovelApiResponse(code=403, message="无权删除", data=None)
    if os.path.exists(novel.file_path):
        os.remove(novel.file_path)
    session.delete(novel)
    session.commit()
    return NovelApiResponse(code=0, message="删除成功", data=None)

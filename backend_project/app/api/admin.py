from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_session
from app.models.user import User
from app.api.auth import get_current_user, require_role

router = APIRouter(prefix="/api/admin", tags=["管理"])


class UserItem(BaseModel):
    id: int
    username: str
    role: str
    avatar: str
    created_at: str


class UserListData(BaseModel):
    users: list[UserItem]
    total: int


class UserListResponse(BaseModel):
    code: int = 0
    message: str = ""
    data: Optional[UserListData] = None


class RoleUpdateRequest(BaseModel):
    role: str  # admin / seed_member / member


class SimpleResponse(BaseModel):
    code: int = 0
    message: str = ""


def _format_user(u: User) -> UserItem:
    return UserItem(
        id=u.id or 0,
        username=u.username,
        role=u.role,
        avatar=u.avatar,
        created_at=u.created_at.isoformat() if isinstance(u.created_at, datetime) else str(u.created_at),
    )


@router.get("/users", response_model=UserListResponse, summary="获取所有用户")
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    _current_user: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """管理员获取所有用户列表"""
    total = session.exec(select(func.count(User.id))).one()
    users = session.exec(select(User).order_by(User.id).offset((page - 1) * page_size).limit(page_size)).all()
    return UserListResponse(code=0, message="获取成功", data=UserListData(users=[_format_user(u) for u in users], total=total))


@router.put("/users/{user_id}/role", response_model=SimpleResponse, summary="修改用户角色")
def update_user_role(
    user_id: int,
    request: RoleUpdateRequest,
    current_user: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """管理员修改用户角色"""
    if request.role not in ("admin", "seed_member", "member"):
        return SimpleResponse(code=400, message="无效的角色值")
    if user_id == current_user.id:
        return SimpleResponse(code=400, message="不能修改自己的角色")
    user = session.get(User, user_id)
    if user is None:
        return SimpleResponse(code=404, message="用户不存在")
    user.role = request.role
    session.add(user)
    session.commit()
    return SimpleResponse(code=0, message="角色修改成功")


@router.get("/users/search", response_model=UserListResponse, summary="搜索用户")
def search_users(
    keyword: str = Query(default="", min_length=1),
    _current_user: User = Depends(require_role("admin")),
    session: Session = Depends(get_session),
):
    """管理员按用户名搜索用户"""
    users = session.exec(select(User).where(User.username.contains(keyword)).order_by(User.id)).all()
    return UserListResponse(code=0, message="搜索完成", data=UserListData(users=[_format_user(u) for u in users], total=len(users)))

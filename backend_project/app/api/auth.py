from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserRegisterRequest, UserRegisterResponse, UserResponse
import bcrypt

router = APIRouter(prefix="/api/auth", tags=["认证"])


def hash_password(password: str) -> str:
    """对密码进行 bcrypt 哈希"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


@router.post("/register", response_model=UserRegisterResponse, summary="用户注册")
def register(request: UserRegisterRequest, session: Session = Depends(get_session)):
    """
    用户注册接口

    - **username**: 账号（3-100个字符）
    - **password**: 密码（6-128个字符）
    """
    # 检查用户名是否已存在
    existing_user = session.query(User).filter(User.username == request.username).first()
    if existing_user:
        return UserRegisterResponse(
            code=400,
            message="该账号已被注册",
            data=None,
        )

    # 创建新用户
    user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserRegisterResponse(
        code=0,
        message="注册成功",
        data=UserResponse(
            id=user.id,
            username=user.username,
            created_at=user.created_at,
        ),
    )

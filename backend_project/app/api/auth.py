from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from jose import JWTError, jwt

from app.database import get_session
from app.models.user import User
from app.models.novel import Novel
from app.models.bookshelf import Bookshelf
from app.models.category import Category
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    LoginData,
    AuthResponse,
    LoginResponse,
    UserStatsResponse,
    UserStatsData,
)
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import bcrypt

router = APIRouter(prefix="/api/auth", tags=["认证"])
security = HTTPBearer()


# ── 密码工具 ──────────────────────────────────────────────

def hash_password(password: str) -> str:
    """对密码进行 bcrypt 哈希"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed: str) -> bool:
    """验证密码是否匹配 bcrypt 哈希"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed.encode("utf-8"))


# ── JWT 工具 ──────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """生成 JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """解码 JWT Token，失败返回 None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    """从请求头 Bearer Token 中提取当前用户"""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="无效的认证令牌")

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="令牌数据无效")

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


ROLE_LEVEL = {"member": 0, "seed_member": 1, "admin": 2}


def require_role(*allowed_roles: str):
    """依赖工厂：仅允许指定角色访问"""

    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user

    return checker


def require_min_role(min_role: str):
    """依赖工厂：角色等级不低于指定级别"""

    def checker(current_user: User = Depends(get_current_user)):
        if ROLE_LEVEL.get(current_user.role, 0) < ROLE_LEVEL.get(min_role, 0):
            raise HTTPException(status_code=403, detail="权限不足")
        return current_user

    return checker


# ── 认证接口 ──────────────────────────────────────────────

@router.post("/register", response_model=AuthResponse, summary="用户注册")
def register(request: UserRegisterRequest, session: Session = Depends(get_session)):
    """用户注册接口"""
    # 检查用户名是否已存在
    existing_user = session.query(User).filter(User.username == request.username).first()
    if existing_user:
        return AuthResponse(code=400, message="该账号已被注册", data=None)

    # 创建新用户
    user = User(
        username=request.username,
        password=request.password,
        password_hash=hash_password(request.password),
        avatar=request.avatar,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return AuthResponse(
        code=0,
        message="注册成功",
        data=UserResponse(
            id=user.id,
            username=user.username,
            role=user.role,
            avatar=user.avatar,
            created_at=user.created_at,
        ),
    )


@router.post("/login", response_model=LoginResponse, summary="用户登录")
def login(request: UserLoginRequest, session: Session = Depends(get_session)):
    """用户登录接口，返回 JWT Token"""
    # 查找用户
    user = session.query(User).filter(User.username == request.username).first()
    if not user:
        return LoginResponse(code=400, message="用户名或密码错误", data=None)

    # 验证密码
    if not verify_password(request.password, user.password_hash):
        return LoginResponse(code=400, message="用户名或密码错误", data=None)

    # 生成 JWT Token
    access_token = create_access_token(data={"user_id": user.id, "username": user.username})

    return LoginResponse(
        code=0,
        message="登录成功",
        data=LoginData(
            token=access_token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                role=user.role,
                avatar=user.avatar,
                created_at=user.created_at,
            ),
        ),
    )


@router.get("/profile", response_model=AuthResponse, summary="获取用户信息")
def profile(
    current_user: User = Depends(get_current_user),
):
    """获取当前登录用户的资料"""
    return AuthResponse(
        code=0,
        message="获取成功",
        data=UserResponse(
            id=current_user.id,
            username=current_user.username,
            role=current_user.role,
            avatar=current_user.avatar,
            created_at=current_user.created_at,
        ),
    )


@router.get("/user/stats", response_model=UserStatsResponse, summary="用户统计")
def user_stats(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """获取当前用户的统计数据"""
    from sqlmodel import func, select

    # 上传的小说数
    novel_count = session.exec(
        select(func.count()).select_from(Novel).where(Novel.user_id == current_user.id)
    ).one()

    # 书架数
    bookshelf_count = session.exec(
        select(func.count()).select_from(Bookshelf).where(Bookshelf.user_id == current_user.id)
    ).one()

    # 分类数
    category_count = session.exec(
        select(func.count()).select_from(Category).where(Category.user_id == current_user.id)
    ).one()

    # 总上传大小
    total_size = session.exec(
        select(func.coalesce(func.sum(Novel.file_size), 0)).where(Novel.user_id == current_user.id)
    ).one()

    return UserStatsResponse(
        code=0,
        message="获取成功",
        data=UserStatsData(
            novel_count=novel_count,
            bookshelf_count=bookshelf_count,
            category_count=category_count,
            total_size=total_size,
        ),
    )

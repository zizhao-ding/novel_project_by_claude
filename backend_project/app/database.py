from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# 导入所有模型，确保 create_all 能创建所有表
from app.models.user import User  # noqa: F401
from app.models.novel import Novel  # noqa: F401

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    """创建数据库表"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """获取数据库会话"""
    with Session(engine) as session:
        yield session

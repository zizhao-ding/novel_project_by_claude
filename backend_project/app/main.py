from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.api.auth import router as auth_router
from app.api.novel import router as novel_router
from app.api.category import router as category_router
from app.api.bookshelf import router as bookshelf_router
from app.api.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理：启动时创建数据库表"""
    create_db_and_tables()
    yield


app = FastAPI(
    title="小说阅读平台 API",
    description="支持图片和文本小说上传及在线阅读的后端服务",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 中间件（允许前端开发时跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(novel_router)
app.include_router(category_router)
app.include_router(bookshelf_router)
app.include_router(admin_router)


@app.get("/", tags=["健康检查"])
def root():
    """健康检查接口"""
    return {"status": "ok", "message": "后端服务运行中"}

"""
种子数据脚本 — 为 test 用户创建假数据小说并加入书架
用法: python seed.py
"""
import os
import sys
from datetime import datetime

# 确保能导入 app 模块
sys.path.insert(0, os.path.dirname(__file__))

from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models.user import User
from app.models.novel import Novel
from app.models.category import Category
from app.models.bookshelf import Bookshelf
from app.api.auth import hash_password


def seed():
    """创建种子数据"""
    # 确保表存在
    create_db_and_tables()

    with Session(engine) as session:
        # ── 1. 创建或获取 test 用户 ──
        user = session.exec(select(User).where(User.username == "test")).first()
        if not user:
            user = User(
                username="test",
                password="123456",
                password_hash=hash_password("123456"),
                role="admin",
                avatar="#66BB6A",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"✅ 创建用户: test (id={user.id}, role=admin)")
        else:
            # 确保已有用户也是 admin
            if user.role != "admin":
                user.role = "admin"
                session.add(user)
                session.commit()
            print(f"ℹ️  用户已存在: test (id={user.id}, role={user.role})")

        # ── 2. 创建分类 ──
        categories_data = [
            ("玄幻", "#e74c3c"),
            ("仙侠", "#3498db"),
            ("奇幻", "#2c3e50"),
            ("游戏", "#f39c12"),
        ]
        cat_map = {}
        for name, color in categories_data:
            cat = session.exec(
                select(Category).where(Category.user_id == user.id, Category.name == name)
            ).first()
            if not cat:
                cat = Category(user_id=user.id, name=name, color=color)
                session.add(cat)
                session.commit()
                session.refresh(cat)
                print(f"✅ 创建分类: {name} (id={cat.id})")
            cat_map[name] = cat

        # ── 3. 创建假数据小说 ──
        novels_data = [
            ("斗破苍穹", 1024000),
            ("凡人修仙传", 2048000),
            ("诡秘之主", 1536000),
            ("全职高手", 896000),
            ("牧神记", 1792000),
            ("大奉打更人", 1280000),
        ]
        novel_objs = []
        for title, size in novels_data:
            novel = session.exec(
                select(Novel).where(Novel.user_id == user.id, Novel.title == title)
            ).first()
            if not novel:
                novel = Novel(
                    user_id=user.id,
                    title=title,
                    file_path=f"uploads/novels/seed_{title}.txt",
                    file_size=size,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(novel)
                session.commit()
                session.refresh(novel)
                print(f"✅ 创建小说: {title} (id={novel.id})")
            novel_objs.append(novel)

        # ── 4. 分配分类 ──
        category_assignments = {
            "斗破苍穹": "玄幻",
            "凡人修仙传": "仙侠",
            "诡秘之主": "奇幻",
            "全职高手": "游戏",
            "牧神记": "玄幻",
            "大奉打更人": "仙侠",
        }
        for novel in novel_objs:
            cat_name = category_assignments.get(novel.title)
            if cat_name and cat_name in cat_map:
                novel.category_id = cat_map[cat_name].id
                session.add(novel)
        session.commit()

        # ── 5. 加入书架 ──
        for novel in novel_objs:
            existing = session.exec(
                select(Bookshelf).where(
                    Bookshelf.user_id == user.id,
                    Bookshelf.novel_id == novel.id,
                )
            ).first()
            if not existing:
                shelf = Bookshelf(user_id=user.id, novel_id=novel.id)
                session.add(shelf)
                print(f"✅ 加入书架: {novel.title}")

        session.commit()
        print("\n🎉 种子数据创建完成！")
        print(f"   用户: test / 123456")
        print(f"   小说: {len(novel_objs)} 本")
        print(f"   分类: {len(cat_map)} 个")


if __name__ == "__main__":
    seed()

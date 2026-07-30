"""EP07 迁移：php artisan make:migration vs Alembic

Laravel：php artisan make:migration 生成迁移文件，up()/down() 改表结构。
FastAPI：用 Alembic 管理迁移（本仓已附最小可跑骨架）。

端点说明：
  POST /ep07/init      —— 开发期 create_all（convenience，生产别用）
  GET  /ep07/alembic   —— 返回 Alembic 命令速查（对照 artisan migrate）

真实迁移请在 fastapi/ 目录执行：
  alembic revision --autogenerate -m "initial"
  alembic upgrade head
"""
from fastapi import APIRouter

from app.db import Base, engine

router = APIRouter()


@router.post("/init")
def init_schema():
    # 开发期一行建好所有表；生产请改用 Alembic 迁移
    Base.metadata.create_all(bind=engine)
    return {"tables": list(Base.metadata.tables.keys()), "hint": "prod: alembic upgrade head"}


@router.get("/alembic")
def alembic_cheatsheet():
    """对照 Laravel 的 artisan migrate 命令速查。"""
    return {
        "laravel": [
            "php artisan make:migration create_posts_table",
            "php artisan migrate",
            "php artisan migrate:rollback",
        ],
        "alembic": [
            "alembic revision --autogenerate -m 'initial'",
            "alembic upgrade head",
            "alembic downgrade -1",
        ],
        "files": {
            "ini": "fastapi/alembic.ini",
            "env": "fastapi/alembic/env.py",
            "versions": "fastapi/alembic/versions/",
        },
    }

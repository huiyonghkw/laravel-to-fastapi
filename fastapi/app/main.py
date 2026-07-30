"""
Laravel ↔ FastAPI 对照学 · 代码骨架（FastAPI 侧）
运行：uvicorn app.main:app --reload
访问 http://127.0.0.1:8000/docs 查看自动生成的 Swagger

每个 EP 一个 router，统一挂到 /epXX 前缀，方便对照查看。
EP00~EP15 全部实现为可运行对照示例；EP12 是测试（见 fastapi/tests/）。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import (
    ep00,
    ep01,
    ep02,
    ep03,
    ep04,
    ep05,
    ep06,
    ep07,
    ep08,
    ep09,
    ep10,
    ep11,
    ep13,
    ep14,
    ep15,
)
from app.db import Base, engine

app = FastAPI(title="Laravel↔FastAPI 对照学", version="0.2.0")

# EP10：真正的全局 ASGI 中间件（对照 Laravel 全局 $middleware）
# 路由级「中间件」用 dependencies=[Depends(...)]，见 ep10.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ORM 相关模型（EP06/EP08）在 import 时已注册到 Base.metadata
# 开发期 convenience：一次性建表。生产请用 Alembic（见 EP07 / alembic/）
Base.metadata.create_all(bind=engine)

app.include_router(ep00.router, prefix="/ep00", tags=["EP00 世界观"])
app.include_router(ep01.router, prefix="/ep01", tags=["EP01 心智模型/DI"])
app.include_router(ep02.router, prefix="/ep02", tags=["EP02 路由"])
app.include_router(ep03.router, prefix="/ep03", tags=["EP03 控制器"])
app.include_router(ep04.router, prefix="/ep04", tags=["EP04 请求响应"])
app.include_router(ep05.router, prefix="/ep05", tags=["EP05 校验/Pydantic"])
app.include_router(ep06.router, prefix="/ep06", tags=["EP06 ORM"])
app.include_router(ep07.router, prefix="/ep07", tags=["EP07 迁移"])
app.include_router(ep08.router, prefix="/ep08", tags=["EP08 事务"])
app.include_router(ep09.router, prefix="/ep09", tags=["EP09 DI进阶"])
app.include_router(ep10.router, prefix="/ep10", tags=["EP10 中间件"])
app.include_router(ep11.router, prefix="/ep11", tags=["EP11 认证"])
app.include_router(ep13.router, prefix="/ep13", tags=["EP13 异步/队列"])
app.include_router(ep14.router, prefix="/ep14", tags=["EP14 部署"])
app.include_router(ep15.router, prefix="/ep15", tags=["EP15 决策树"])


@app.get("/")
def root():
    return {
        "series": "Laravel↔FastAPI 对照学",
        "baseline": {"laravel": "13", "fastapi": "0.140.13"},
        "docs": "/docs",
        "note": "Laravel 侧为源码对照（laravel/），不要求 composer install 即可阅读。",
    }

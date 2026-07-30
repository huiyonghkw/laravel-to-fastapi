"""
Laravel ↔ FastAPI 对照学 · 免费试读骨架（FastAPI 侧）
试读范围：EP00 世界观 · EP02 路由 · EP05 校验
运行：uvicorn app.main:app --reload → http://127.0.0.1:8000/docs
完整 15 期见付费私有仓 laravel-to-fastapi-pro
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import ep00, ep02, ep05

app = FastAPI(
    title="Laravel↔FastAPI 对照学（试读）",
    version="1.0.0",
    description="免费试读 3 期：EP00 / EP02 / EP05。完整系列见付费仓。",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ep00.router, prefix="/ep00", tags=["EP00 世界观"])
app.include_router(ep02.router, prefix="/ep02", tags=["EP02 路由"])
app.include_router(ep05.router, prefix="/ep05", tags=["EP05 校验/Pydantic"])


@app.get("/")
def root():
    return {
        "series": "Laravel↔FastAPI 对照学",
        "tier": "oss-trial",
        "baseline": {"laravel": "13", "fastapi": "0.140.13"},
        "free_eps": ["ep00", "ep02", "ep05"],
        "docs": "/docs",
        "upgrade": "Full 15-ep series: private repo laravel-to-fastapi-pro",
    }

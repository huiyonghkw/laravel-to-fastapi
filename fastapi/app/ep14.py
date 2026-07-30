"""EP14 部署：Nginx + PHP-FPM vs Uvicorn / Gunicorn (ASGI)

Laravel：Nginx 反代到 PHP-FPM（同步进程池）。
FastAPI：Uvicorn 跑 ASGI（或 Gunicorn + Uvicorn worker 多进程）。
本文件不写部署逻辑，只暴露一个读运行环境信息的端点，方便确认「跑在哪」。
真正部署见仓库 fastapi/Dockerfile + 下方命令。
"""
import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/env")
def env():
    return {
        "worker": os.getenv("WORKERS", "1"),
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": os.getenv("PORT", "8000"),
    }


# ---- 部署命令（对照 Laravel 的 php artisan serve / Nginx 配置） ----
# 开发： uvicorn app.main:app --reload
# 生产： gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4
# 容器： docker build -t laravel-fastapi -f fastapi/Dockerfile . && docker run -p 8000:8000 laravel-fastapi

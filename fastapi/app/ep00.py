"""EP00 世界观：框架哲学与请求生命周期对照（对照 Laravel routes/api.php 的 /hello）"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
def hello():
    # FastAPI 请求生命周期（ASGI）：
    #   接收请求 -> 路由匹配 -> 解析依赖(Depends) -> 调用路径操作函数
    #   -> 用 Pydantic 序列化返回值为 JSON -> 发出响应
    # 对照 Laravel：HTTP 内核 -> 路由 -> 中间件 -> 控制器 -> 响应（同步、FPM 进程模型）
    return {
        "framework": "FastAPI",
        "msg": "Hello from an API-first micro-framework (ASGI, async-native)",
    }

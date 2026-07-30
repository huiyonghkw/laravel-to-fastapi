"""EP10 中间件：Laravel middleware vs FastAPI 依赖中间件 / ASGI 中间件

Laravel：$middleware 组 / 路由中间件，在请求前后统一插逻辑。
FastAPI：
  - 路由级「中间件」用 dependencies=[Depends(...)]（最常用，等价路由中间件）
  - 真正的全局 ASGI 中间件用 app.add_middleware()（如 CORSMiddleware），见 main.py
"""
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

router = APIRouter()


def log_request(req: Request):
    # 这里可记日志；返回 None 表示放行
    # 真实项目里也可 raise HTTPException 直接拦截
    req.state.logged = True
    return None


def require_x_token(x_token: str | None = Header(default=None)):
    """路由级鉴权依赖：等价 Laravel Route::middleware('auth')->..."""
    if not x_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="missing x-token")
    return x_token


# 路由级中间件：等价 Laravel Route::middleware('log')->get(...)
@router.get("/secure", dependencies=[Depends(log_request)])
def secure():
    return {"ok": True, "hint": "全局 CORS 中间件见 main.py 的 add_middleware(CORSMiddleware)"}


@router.get("/token-gate", dependencies=[Depends(require_x_token)])
def token_gate():
    return {"ok": True, "msg": "x-token accepted"}

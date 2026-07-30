"""EP01 心智模型：依赖注入 (Depends) + 异步 (async) 对照 Laravel 服务容器 / 同步闭包"""
from fastapi import APIRouter, Depends
import asyncio

router = APIRouter()


# 类比 Laravel 的服务容器：用生成器管“连接”的生命周期（yield = 请求级作用域）
def get_db():
    db = {"conn": "fake-connection"}  # 真实项目里换成 Session() / 连接池
    try:
        yield db                      # 请求期间注入这个 db；请求结束走 finally
    finally:
        pass                          # 真实项目里这里 db.close()，等价于容器的析构


@router.get("/user/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):
    # Depends(get_db) 就是 FastAPI 的“依赖注入”：
    #   等价于 Laravel 在控制器构造函数里类型提示，容器自动帮你 new 好传进来。
    return {"user_id": user_id, "db": db["conn"]}


# 异步：async def + await，等 I/O 时让出进程去接别的请求（Laravel 默认同步阻塞）
@router.get("/slow")
async def slow_task():
    await asyncio.sleep(0.1)          # 模拟 I/O（查库 / 调接口）；await 时事件循环去处理别的请求
    return {"msg": "done without blocking the event loop"}


# 嵌套依赖：Depends 套 Depends，等价于 Laravel 容器解析链（AuthService -> UserService）
def get_token():
    return "fake-token"


def get_current_user(token: str = Depends(get_token)):
    return {"user": "alice", "token": token}     # 真实项目里这里 decode token 取用户


@router.get("/me")
def me(u: dict = Depends(get_current_user)):
    return u


# 并发：用 asyncio.gather 同时发多个 I/O，比顺序 await 快（Laravel 同步做不到）
async def _fetch(x: str):
    await asyncio.sleep(0.05)                     # 模拟一次外部调用
    return x


@router.get("/batch")
async def batch():
    a, b = await asyncio.gather(_fetch("A"), _fetch("B"))   # 两个调用并发进行
    return {"a": a, "b": b}

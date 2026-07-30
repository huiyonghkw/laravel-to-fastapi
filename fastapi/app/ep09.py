"""EP09 依赖注入进阶：容器绑定/单例 vs Depends 嵌套 + 生命周期

Laravel：App::bind() / App::singleton() 把接口绑到实现，容器解析。
FastAPI：依赖可以是函数或类；模块级实例 ≈ singleton；嵌套 Depends 等价解析链；
         同一个请求内默认缓存（use_cache=False 关掉）。
"""
from fastapi import APIRouter, Depends

router = APIRouter()


class Counter:
    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return self.n


# 模块级实例 = Laravel 的 App::singleton()（整个进程一份）
_counter = Counter()


def get_counter():
    return _counter


# 嵌套依赖：依赖里再 Depends，等价 Laravel 的解析链
def get_config():
    return {"env": "dev"}


def get_db_url(cfg: dict = Depends(get_config)):
    return f"db://{cfg['env']}"


@router.get("/count")
def count(c: Counter = Depends(get_counter)):
    # 同一进程内 Counter 是同一份 → 计数累加，等价 singleton
    return {"n": c.next()}


@router.get("/db-url")
def db_url(url: str = Depends(get_db_url)):
    return {"url": url}

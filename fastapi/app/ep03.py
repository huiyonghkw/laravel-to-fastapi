"""EP03 控制器 vs 路径操作函数

Laravel：逻辑收进 Controller 类（app/Http/Controllers/Api/UserController.php）。
FastAPI：函数即「路径操作」，无需 Controller 类；用 router 把一组函数收在一起，
         组织方式等价于 Laravel 的一个 Controller。
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def list_users():
    # 对照 Laravel: UserController@index
    return {"users": []}


@router.get("/users/{uid}")
def show_user(uid: int):
    # 对照 Laravel: UserController@show，{uid} 自动按 int 解析
    return {"uid": uid}


@router.post("/users")
def store_user():
    # 对照 Laravel: UserController@store
    return {"created": True}


@router.put("/users/{uid}")
def update_user(uid: int):
    # 上手练习答案示例（EP03 HTML 练习）
    return {"uid": uid, "updated": True}

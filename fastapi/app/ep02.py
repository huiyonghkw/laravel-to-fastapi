"""EP02 路由：APIRouter 分组 + 依赖中间件，对照 Laravel Route:: 分组与中间件"""
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


# 模拟“当前用户”——等价于 Laravel 的 auth 中间件（解析 Bearer Token）
def get_current_user():
    return {"user": "alice"}            # 真实项目里这里 decode token


# ---- 公开路由：直接挂在 router 上 ----
@router.get("/health")
def health():
    return {"ok": True}


# ---- 分组路由：所有 /posts/* 归到一组，并统一加 auth 依赖 ----
# 等价于 Laravel：
#   Route::middleware('auth:sanctum')
#        ->prefix('posts')
#        ->group(function () {
#            Route::get('/', [PostController::class, 'index']);
#            Route::post('/', [PostController::class, 'store']);
#        });
posts = APIRouter(prefix="/posts", tags=["posts"], dependencies=[Depends(get_current_user)])


@posts.get("")                      # GET /ep02/posts
def list_posts():
    return {"posts": []}


@posts.post("")                     # POST /ep02/posts
def create_post():
    return {"created": True}


@posts.get("/{post_id}")            # GET /ep02/posts/{id}
def get_post(post_id: int):
    # 路径参数按类型提示自动校验/转换（int），等价于 Laravel 隐式绑定
    if post_id <= 0:
        raise HTTPException(status_code=404, detail="not found")
    return {"post_id": post_id}


router.include_router(posts)

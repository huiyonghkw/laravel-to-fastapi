"""EP04 请求与响应对象

Laravel：Illuminate\\Http\\Request / Response。
FastAPI： Request 读入站数据，返回 dict 自动变 JSON，或显式用 JSONResponse 控制状态码/头。
"""
from fastapi import APIRouter, Request, Header
from fastapi.responses import JSONResponse
from typing import Optional

router = APIRouter()


@router.get("/echo")
def echo(req: Request, x_token: Optional[str] = Header(None)):
    # 读请求：URL / query / header / body 都在 Request 上
    # 对照 Laravel: $request->url() / $request->query() / $request->header('x-token')
    return {
        "path": req.url.path,
        "token": x_token,
    }


@router.get("/custom")
def custom():
    # 自定义响应：状态码 + 自定义头，对照 Laravel response()->json($d, 201)->header(...)
    return JSONResponse(
        status_code=201,
        content={"ok": True},
        headers={"x-powered-by": "fastapi"},
    )

"""EP11 认证授权：Sanctum / Passport vs fastapi.security

Laravel：Sanctum 发 token、auth:sanctum 中间件保护路由。
FastAPI：OAuth2PasswordBearer 取 Bearer token，Depends(get_current_user) 保护路由。

⚠️ 本文件是**教学 stub**：token 用明文演示，不是生产 JWT。
真实项目用密码哈希 + JWT（PyJWT）/ OAuth2 完整流。这里只讲清「发 token → 护路由」同构。
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="/ep11/login")

# 演示用假用户表（对照 Laravel users + Hash::check）
_USERS = {"alice": {"password": "secret", "name": "Alice"}}


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_current_user(token: str = Depends(oauth2)):
    # stub：token 格式约定为 "user:<username>"；生产请换成 JWT decode
    if not token.startswith("user:"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    username = token.removeprefix("user:")
    if username not in _USERS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="unknown user")
    return {"user": username, "name": _USERS[username]["name"]}


@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends()):
    # Swagger「Authorize」按钮会打这个表单接口（username/password）
    user = _USERS.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="bad credentials")
    return TokenOut(access_token=f"user:{form.username}")


@router.get("/me")
def me(u: dict = Depends(get_current_user)):
    return u

"""EP05 校验与序列化：Pydantic 对照 Laravel Form Request + API Resource

一个 Pydantic model 同时承担三件事（Laravel 要分三个东西做）：
  1) 请求校验        —— 等价于 Form Request 的 rules()
  2) 响应序列化      —— 等价于 API Resource 的 toArray()（response_model）
  3) 自动生成文档     —— Swagger schema 从类型提示推导
"""
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0, le=150)


class UserOut(BaseModel):
    """响应模型：只暴露对外字段（对照 Laravel API Resource）。"""

    id: int
    name: str
    email: EmailStr


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate):
    # 缺字段 / email 非法 → 自动 422（对照 Laravel validate 失败）
    # response_model=UserOut → 只序列化 id/name/email，内部字段不会漏出
    return UserOut(id=1, name=payload.name, email=payload.email)


@router.get("/users/demo", response_model=UserOut)
def demo_user():
    return UserOut(id=1, name="alice", email="alice@example.com")

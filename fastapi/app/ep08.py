"""EP08 事务与关联查询：DB::transaction vs session.begin()

Laravel：DB::transaction(fn () => ...)，异常自动回滚。
FastAPI：with db.begin(): 上下文管理器，等效事务。

本页用**同步 Session**（对标 Eloquent）。文案里的「async with session」
指 async SQLAlchemy 进阶写法，不在本演示范围内——别混读。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Integer, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db import Base, get_db

router = APIRouter()


class Order(Base):
    __tablename__ = "ep08_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)


class OrderItem(Base):
    __tablename__ = "ep08_order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer)
    sku: Mapped[str] = mapped_column()
    qty: Mapped[int] = mapped_column(Integer, default=1)


class OrderIn(BaseModel):
    amount: int = Field(gt=0)
    sku: str = "demo"
    qty: int = Field(default=1, gt=0)
    fail: bool = False  # True 时故意抛错，演示自动回滚


@router.post("/orders")
def create_order(payload: OrderIn, db: Session = Depends(get_db)):
    # 对照 Laravel: DB::transaction(function () { ... });
    # 异常自动 rollback；成功则 commit
    try:
        with db.begin():
            o = Order(amount=payload.amount)
            db.add(o)
            db.flush()  # 拿到 o.id，供子表外键使用
            db.add(OrderItem(order_id=o.id, sku=payload.sku, qty=payload.qty))
            if payload.fail:
                raise RuntimeError("simulated failure → rollback")
            order_id = o.id
            amount = o.amount
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {"id": order_id, "amount": amount, "rolled_back": False}


@router.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    rows = db.execute(select(Order)).scalars().all()
    return [{"id": o.id, "amount": o.amount} for o in rows]

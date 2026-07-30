"""EP06 ORM：Eloquent vs SQLAlchemy 2.0

Laravel：Model 即表，Post::with('comments')->get()。
FastAPI：用 SQLAlchemy 2.0 风格定义模型（Mapped/mapped_column），
         查询用 select() + session.execute（不要再用 legacy db.query()）。

本页用同步 Session，对标 Eloquent 默认同步；不要和 async SQLAlchemy 混读。
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped, Session, joinedload, mapped_column, relationship

from app.db import Base, get_db

router = APIRouter()


class Post(Base):
    __tablename__ = "ep06_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    # relationship 等价于 Eloquent 的 comments() 关联
    comments: Mapped[list[Comment]] = relationship(back_populates="post")


class Comment(Base):
    __tablename__ = "ep06_comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey("ep06_posts.id"))
    post: Mapped[Post] = relationship(back_populates="comments")


@router.post("/seed")
def seed(db: Session = Depends(get_db)):
    """塞两条演示数据，方便 GET /posts 有东西看。"""
    if db.execute(select(Post)).scalars().first():
        return {"seeded": False, "msg": "already has data"}
    p = Post(title="hello orm")
    p.comments.append(Comment(body="first comment"))
    db.add(p)
    db.commit()
    return {"seeded": True, "post_id": p.id}


@router.get("/posts")
def list_posts(db: Session = Depends(get_db)):
    # Eloquent: Post::with('comments')->get()
    # SQLAlchemy 2.0: select + joinedload（eager load，避免 N+1）
    stmt = select(Post).options(joinedload(Post.comments))
    rows = db.execute(stmt).unique().scalars().all()
    return [
        {"id": p.id, "title": p.title, "comments": [c.body for c in p.comments]}
        for p in rows
    ]


@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    stmt = select(Post).options(joinedload(Post.comments)).where(Post.id == post_id)
    p = db.execute(stmt).unique().scalars().first()
    if not p:
        raise HTTPException(status_code=404, detail="not found")
    return {"id": p.id, "title": p.title, "comments": [c.body for c in p.comments]}

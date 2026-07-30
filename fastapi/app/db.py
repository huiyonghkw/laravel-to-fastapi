"""共享：SQLAlchemy 引擎 / 会话 / Base（EP06 ORM、EP07 迁移、EP08 事务 复用）

用内存 SQLite（StaticPool 保持单连接）做演示，无需真实数据库即可跑通。
真实项目把 DATABASE_URL 换成 PostgreSQL/MySQL 连接串即可。

注意：本仓演示用**同步 Session**（对标 Eloquent 默认同步心智）。
async SQLAlchemy（AsyncSession）是另一条进阶线，别和本页示例混读。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = "sqlite://"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 声明式基类（替代旧版 declarative_base()）。"""


def get_db():
    """请求级数据库会话，等价于 Laravel 服务容器里注入的 DB 连接。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

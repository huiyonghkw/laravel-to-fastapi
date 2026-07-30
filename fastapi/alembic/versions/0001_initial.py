"""initial ep06/ep08 tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-30

对照 Laravel: php artisan make:migration create_posts_table 的 up()/down()。
本文件是手写最小示例；真实项目多用 `alembic revision --autogenerate`。
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ep06_posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
    )
    op.create_table(
        "ep06_comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("body", sa.String(255), nullable=False),
        sa.Column("post_id", sa.Integer(), sa.ForeignKey("ep06_posts.id"), nullable=False),
    )
    op.create_table(
        "ep08_orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("amount", sa.Integer(), nullable=False),
    )
    op.create_table(
        "ep08_order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ep08_order_items")
    op.drop_table("ep08_orders")
    op.drop_table("ep06_comments")
    op.drop_table("ep06_posts")

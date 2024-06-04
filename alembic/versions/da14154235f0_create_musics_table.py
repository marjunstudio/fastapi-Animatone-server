"""create_musics_table

Revision ID: da14154235f0
Revises: 5f445e5908e6
Create Date: 2024-06-03 07:34:45.396128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da14154235f0'
down_revision: Union[str, None] = '5f445e5908e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "composers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("furigana", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # musicテーブルにcomposer_idカラムを追加
    op.add_column("musics", sa.Column("composer_id", sa.Integer(), nullable=True))
    
    # musicテーブルのcomposer_idカラムに外部キー制約を追加
    op.create_foreign_key(
        "fk_musics_composer_id",
        "musics",
        "composers",
        ["composer_id"],
        ["id"],
    )

def downgrade():
    # 外部キー制約を削除
    op.drop_constraint("fk_musics_composer_id", "musics", type_="foreignkey")
    
    # musicテーブルからcomposer_idカラムを削除
    op.drop_column("musics", "composer_id")
    
    op.drop_table("composers")

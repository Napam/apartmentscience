"""add test table

Revision ID: 7d40a7699440
Revises: 5b975c54a3ee
Create Date: 2022-03-03 20:02:10.338274

"""
from enum import auto
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7d40a7699440"
down_revision = "5b975c54a3ee"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "test",
        sa.Column("_id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("_str", sa.UnicodeText),
        sa.Column("_int", sa.Integer),
        sa.Column("_float", sa.Float),
    )


def downgrade():
    op.drop_table("test")

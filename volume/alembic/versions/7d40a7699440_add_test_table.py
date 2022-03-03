"""add test table

Revision ID: 7d40a7699440
Revises: 5b975c54a3ee
Create Date: 2022-03-03 20:02:10.338274

"""
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
        sa.Column("text", sa.UnicodeText),
        sa.Column("int", sa.Integer),
        sa.Column("float", sa.Float),
    )


def downgrade():
    op.drop_table("test")

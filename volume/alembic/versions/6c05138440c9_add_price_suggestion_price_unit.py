"""add price suggestion price unit

Revision ID: 6c05138440c9
Revises: 7ab72b49bb0f
Create Date: 2024-03-24 19:17:50.165467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c05138440c9'
down_revision = '7ab72b49bb0f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("price_suggestion_price_unit", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "price_suggestion_price_unit")

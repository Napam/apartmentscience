"""add price total price unit

Revision ID: 30f71501ccbf
Revises: 6c05138440c9
Create Date: 2024-03-24 19:20:04.222021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30f71501ccbf'
down_revision = '6c05138440c9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("price_total_price_unit", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "price_total_price_unit")

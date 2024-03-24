"""add price shared cost price unit

Revision ID: d6e0d8736e4c
Revises: 30f71501ccbf
Create Date: 2024-03-24 19:20:54.280287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6e0d8736e4c'
down_revision = '30f71501ccbf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("price_shared_cost_price_unit", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "price_shared_cost_price_unit")

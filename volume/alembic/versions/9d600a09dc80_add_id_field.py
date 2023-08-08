"""add_id_field

Revision ID: 9d600a09dc80
Revises: 80ac25aa2e22
Create Date: 2023-08-08 16:51:01.427520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d600a09dc80'
down_revision = '80ac25aa2e22'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("id", sa.Integer))


def downgrade():
    op.drop_column("preview", "id")

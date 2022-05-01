"""add column for ad_type

Revision ID: 80ac25aa2e22
Revises: 0596611f8c80
Create Date: 2022-05-01 19:31:34.184303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "80ac25aa2e22"
down_revision = "0596611f8c80"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("ad_type", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "ad_type")

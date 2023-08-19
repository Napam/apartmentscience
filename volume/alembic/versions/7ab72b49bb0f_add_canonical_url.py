"""add canonical_url

Revision ID: 7ab72b49bb0f
Revises: 155270a7cd40
Create Date: 2023-08-19 21:46:58.467766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ab72b49bb0f'
down_revision = '155270a7cd40'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("canonical_url", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "canonical_url)")

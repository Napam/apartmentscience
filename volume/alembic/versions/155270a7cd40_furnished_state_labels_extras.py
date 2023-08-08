"""furnished_state, labels, extras

Revision ID: 155270a7cd40
Revises: 9d600a09dc80
Create Date: 2023-08-08 17:17:23.892390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '155270a7cd40'
down_revision = '9d600a09dc80'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("preview", sa.Column("labels", sa.UnicodeText))
    op.add_column("preview", sa.Column("extras", sa.UnicodeText))
    op.add_column("preview", sa.Column("furnished_state", sa.UnicodeText))


def downgrade():
    op.drop_column("preview", "labels")
    op.drop_column("preview", "extras")
    op.drop_column("preview", "furnished_state")

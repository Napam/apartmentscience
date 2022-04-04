"""create preview_meta table

Revision ID: 0596611f8c80
Revises: 7d40a7699440
Create Date: 2022-04-01 19:30:58.380132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0596611f8c80"
down_revision = "7d40a7699440"
branch_labels = None
depends_on = None


def upgrade():
    # Comments represents field that 6are in response, but not used
    op.create_table(
        "preview_meta",
        sa.Column("_batch", sa.Integer, primary_key=True),
        sa.Column("batch_date", sa.DateTime),
    )

    op.execute("INSERT INTO preview_meta SELECT _batch, MIN(_created) FROM preview GROUP BY _batch")


def downgrade():
    op.drop_table("preview_meta")

"""create preview table

Revision ID: 5b975c54a3ee
Revises: 
Create Date: 2022-01-06 20:11:37.954841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b975c54a3ee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Comments represents field that are in response, but not used
    op.create_table(
        "preview",
        sa.Column("session", sa.Integer),
        sa.Column("type", sa.Text),
        sa.Column("ad_id", sa.Integer),
        sa.Column("main_search_key", sa.Text),
        sa.Column("heading", sa.UnicodeText),
        sa.Column("location", sa.UnicodeText),
        # sa.Column("image"),
        # sa.Column("flags"),
        # sa.Column("styling"),
        sa.Column("timestamp", sa.Integer),
        sa.Column("price_suggestion", sa.Float),
        sa.Column("price_suggestion_currency", sa.Text),
        sa.Column("price_total", sa.Float),
        sa.Column("price_total_currency", sa.Text),
        sa.Column("price_shared_cost", sa.Float),
        sa.Column("price_shared_cost_currency", sa.Text),
        sa.Column("area_range_size_from", sa.Float),
        sa.Column("area_range_size_to", sa.Float),
        sa.Column("area_range_size_unit", sa.Text),
        sa.Column("area_range_size_description", sa.Text),
        sa.Column("area_plot_size", sa.Float),
        sa.Column("area_plot_unit", sa.Text),
        sa.Column("area_plot_description", sa.UnicodeText),
        sa.Column("organisation_name", sa.UnicodeText),
        sa.Column("number_of_bedrooms", sa.Integer),
        sa.Column("owner_type_description", sa.UnicodeText),
        sa.Column("property_type_description", sa.UnicodeText),
        # sa.Column("viewing_times"),
        sa.Column("coordinates_lat", sa.Float),
        sa.Column("coordinates_lon", sa.Float),
        # sa.Column("image_urls"),
        sa.Column("ad_link", sa.Text),
    )


def downgrade():
    op.drop_table("preview")

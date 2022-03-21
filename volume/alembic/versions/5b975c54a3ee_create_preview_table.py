"""create preview table

Revision ID: 5b975c54a3ee
Revises: 
Create Date: 2022-01-06 20:11:37.954841

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "5b975c54a3ee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Comments represents field that 6are in response, but not used
    op.create_table(
        "preview",
        sa.Column("_id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("_created", sa.DateTime, server_default=sa.func.now()),
        sa.Column("_last_updated", sa.DateTime, onupdate=sa.func.now()),
        sa.Column("_batch", sa.Integer),
        sa.Column("type", sa.UnicodeText),
        sa.Column("ad_id", sa.Integer),
        sa.Column("main_search_key", sa.UnicodeText),
        sa.Column("heading", sa.UnicodeText),
        sa.Column("location", sa.UnicodeText),
        sa.Column("image_url", sa.UnicodeText),
        sa.Column("image_path", sa.UnicodeText),
        sa.Column("image_height", sa.Integer),
        sa.Column("image_width", sa.Integer),
        sa.Column("image_aspect_ratio", sa.Float),
        sa.Column("flags", sa.UnicodeText),
        sa.Column("styling", sa.UnicodeText),
        sa.Column("timestamp", sa.Integer),
        sa.Column("logo_url", sa.UnicodeText),
        sa.Column("logo_path", sa.UnicodeText),
        sa.Column("price_suggestion_amount", sa.Integer),
        sa.Column("price_suggestion_currency_code", sa.UnicodeText),
        sa.Column("price_total_amount", sa.Integer),
        sa.Column("price_total_currency_code", sa.UnicodeText),
        sa.Column("price_shared_cost_amount", sa.Integer),
        sa.Column("price_shared_cost_currency_code", sa.UnicodeText),
        sa.Column("area_range_size_from", sa.Integer),
        sa.Column("area_range_size_to", sa.Integer),
        sa.Column("area_range_unit", sa.UnicodeText),
        sa.Column("area_range_description", sa.UnicodeText),
        sa.Column("area_plot_size", sa.Integer),
        sa.Column("area_plot_unit", sa.UnicodeText),
        sa.Column("area_plot_description", sa.UnicodeText),
        sa.Column("organisation_name", sa.UnicodeText),
        sa.Column("local_area_name", sa.UnicodeText),
        sa.Column("number_of_bedrooms", sa.Integer),
        sa.Column("owner_type_description", sa.UnicodeText),
        sa.Column("property_type_description", sa.UnicodeText),
        sa.Column("viewing_times", sa.UnicodeText),
        sa.Column("coordinates_lat", sa.Float),
        sa.Column("coordinates_lon", sa.Float),
        sa.Column("image_urls", sa.UnicodeText),
        sa.Column("ad_link", sa.UnicodeText),
        sa.Column("price_range_suggestion_amount_from", sa.Integer),
        sa.Column("price_range_suggestion_amount_to", sa.Integer),
        sa.Column("price_range_suggestion_currency_code", sa.UnicodeText),
        sa.Column("price_range_total_amount_from", sa.Integer),
        sa.Column("price_range_total_amount_to", sa.Integer),
        sa.Column("price_range_total_currency_code", sa.UnicodeText),
        sa.Column("bedrooms_range_start", sa.Integer),
        sa.Column("bedrooms_range_end", sa.Integer),
        sa.Column("area_size", sa.Integer),
        sa.Column("area_unit", sa.UnicodeText),
        sa.Column("area_description", sa.UnicodeText),
    )


def downgrade():
    op.drop_table("preview")

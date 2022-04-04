from dataclasses import dataclass, field
from typing import Any
import sqlalchemy as sa
from sqlalchemy import orm, func
import datetime

mapper_registry = orm.registry()


@dataclass
class FinnLocationFilter:
    display_name: str
    name: str
    value: str
    hits: int
    filter_items: list["FinnLocationFilter"]
    selected: bool

    def getQueryParams(self) -> dict:
        return {"location": self.value}


@dataclass
class Paging:
    param: str
    current: float
    last: float


@dataclass
class FinnResponse:
    docs: list[dict[str, str | float]]
    filters: list[dict[str, Any]]
    metadata: list[dict[str, Any]]
    mapUrl: str
    isOdin: bool
    pageMetadata: list[dict[str, Any]]


@mapper_registry.mapped
@dataclass
class PreviewMeta:
    __table__ = sa.Table(
        "preview_meta",
        mapper_registry.metadata,
        sa.Column("_batch", sa.Integer, primary_key=True),
        sa.Column("batch_date", sa.DateTime),
    )
    _batch: int
    batch_date: datetime.datetime


@mapper_registry.mapped
@dataclass
class Doc:
    __table__ = sa.Table(
        "preview",
        mapper_registry.metadata,
        sa.Column("_id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("_created", sa.DateTime, server_default=func.now()),
        sa.Column("_last_updated", sa.DateTime, onupdate=func.now()),
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
    _id: int = field(init=False)
    _last_updated: datetime.datetime = field(init=False)
    _batch: int = None
    type: str = None
    ad_id: int = None
    main_search_key: str = None
    heading: str = None
    location: str = None
    image_url: str = None
    image_path: str = None
    image_height: int = None
    image_width: int = None
    image_aspect_ratio: float | int = None
    flags: list = None
    styling: list = None
    timestamp: int = None
    logo_url: str = None
    logo_path: str = None
    price_suggestion_amount: int = None
    price_suggestion_currency_code: str = None
    price_total_amount: int = None
    price_total_currency_code: str = None
    price_shared_cost_amount: int = None
    price_shared_cost_currency_code: str = None
    area_range_size_from: None | int = None
    area_range_size_to: None | int = None
    area_range_unit: str = None
    area_range_description: str = None
    area_plot_size: int = None
    area_plot_unit: str = None
    area_plot_description: str = None
    organisation_name: str = None
    local_area_name: str = None
    number_of_bedrooms: int = None
    owner_type_description: str = None
    property_type_description: str = None
    viewing_times: list = None
    coordinates_lat: float | int = None
    coordinates_lon: float | int = None
    image_urls: list = None
    ad_link: str = None
    price_range_suggestion_amount_from: int = None
    price_range_suggestion_amount_to: int = None
    price_range_suggestion_currency_code: str = None
    price_range_total_amount_from: None | int = None
    price_range_total_amount_to: None | int = None
    price_range_total_currency_code: str = None
    bedrooms_range_start: int = None
    bedrooms_range_end: int = None
    area_size: int = None
    area_unit: str = None
    area_description: str = None

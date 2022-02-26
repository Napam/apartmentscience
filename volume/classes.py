from dataclasses import dataclass, fields, _MISSING_TYPE
from os import times
from typing import Any


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


@dataclass
class Doc:
    type: str = None
    ad_id: int = None
    main_search_key: str = None
    heading: str = None
    location: str = None
    image_url: str = None
    image_path: str = None
    image_height: int = None
    image_width: int = None
    image_aspect_ratio: float = None
    flags: str = None
    styling: str = None
    timestamp: int = None
    logo_url: str = None
    logo_path: str = None
    price_range_suggestion_amount: int = None
    price_range_suggestion_currency: str = None
    price_range_total_amount_from: int = None
    price_range_total_amount_to: int = None
    price_range_total_currency_code: str = None
    price_suggestion_amount: int = None
    price_suggestion_currency_code: str = None
    price_total_amount: int = None
    price_total_currency: str = None
    price_shared_cost_amount: int = None
    price_shared_cost_currency: str = None
    area_range_size_from: int = None
    area_range_size_to: int = None
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
    viewing_times: str = None
    coordinates_lat: float = None
    coordinates_lon: float = None
    image_urls: str = None
    bedrooms_range_start: int = None
    bedrooms_range_end: int = None
    ad_link: str = None
    area: int = None

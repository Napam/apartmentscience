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
    image: dict[str, str | float] = None
    flags: list[str] = None
    styling: list[str] = None
    timestamp: int = None
    logo: dict[str, str] = None
    price_range_suggestion: dict[str, int | str] = None
    price_range_total: dict[str, int | str] = None
    price_suggestion: dict[str, str | float] = None
    price_total: dict[str, str | float] = None
    price_shared_cost: dict[str, str | float] = None
    area_range: dict[str, str | float] = None
    area_plot: dict[str, str | float] = None
    organisation_name: str = None
    local_area_name: str = None
    number_of_bedrooms: int = None
    owner_type_description: str = None
    property_type_description: str = None
    viewing_times: list[str] = None
    coordinates: dict[str, float] = None
    image_urls: list[str] = None
    bedrooms_range: dict[str, int] = None
    ad_link: str = None
    area: int = None

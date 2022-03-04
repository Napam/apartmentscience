import json
from typing import Iterable
import requests
import utils
import classes
import time
import logging
import os
import pathlib
import shutil
import random
from pprint import pprint
from classes import Doc
import sqlalchemy as sa

engine = sa.create_engine("sqlite:///test.db", echo=True, future=True)

TMP_DIR = pathlib.Path("data") / "apartmentscience" / "indexjsons"

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

URL = "https://www.finn.no/api/search-qf"


def getParams(page: int):
    return {
        "searchkey": "SEARCH_ID_REALESTATE_HOMES",
        # "lat": "60.386516342860716",
        # "lon": "5.32861852263332",
        # "radius": 8000,
        # "sort": "PUBLISHED_DESC",
        # "location": "1.22046.20220",
        "page": page,
    }


def clearTempdir():
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)


def storeResponseInTempdir(response: dict):
    TMP_DIR.mkdir(exist_ok=True, parents=True)
    filename = "response" + utils.isoNow() + ".json"
    (TMP_DIR / filename).write_text(json.dumps(response, indent=2))
    logger.info(f"Stored response {TMP_DIR / filename}")


def getResponse(params: dict, mock: bool = False):
    logger.debug(f"getResponse with params: {params}")
    if mock:
        with open(os.path.join("mock", "response.json"), "r") as f:
            responseJson = json.load(f)
    else:
        response = requests.get(URL, params)
        responseJson = response.json()
    return responseJson


def obtainRawIndexData():
    responseJson = getResponse(getParams(1))
    logger.info("Start obtainRawIndexData")
    logger.info(f"Sucessfully obtained first response")

    clearTempdir()
    storeResponseInTempdir(responseJson)

    paging = classes.Paging(**responseJson["metadata"]["paging"])
    numberOfPages = paging.last
    logger.info(f"Total number of pages: {numberOfPages}")
    for i in range(2, numberOfPages + 1):
        params = getParams(i)
        responseJson = getResponse(params)
        storeResponseInTempdir(responseJson)

        waitTime = 0.2 + random.random()
        logger.info(f"Waiting {waitTime}s before next call")
        time.sleep(waitTime)


def docs(flatten: bool = True):
    for file in os.listdir(TMP_DIR):
        with open(os.path.join(TMP_DIR, file), "r") as f:
            docs: list[dict] = json.load(f)["docs"]
            for doc in docs:
                yield utils.flattenDict(doc) if flatten else doc


def storeIndexData():
    """
    Assumes index data is available (generated from obtainRawIndexData)
    """
    for doc in docs():
        pprint(vars(Doc(**utils.flattenDict(doc))))
        conn: sa.engine.Connection
        with engine.connect() as conn:
            conn.execute(
                sa.text(
                    """
                INSERT INTO preview (
                    type,
                    ad_id,
                    main_search_key,
                    heading,
                    location,
                    image_url,
                    image_path,
                    image_height,
                    image_width,
                    image_aspect_ratio,
                    flags,
                    styling,
                    timestamp,
                    logo_url,
                    logo_path,
                    price_suggestion_amount,
                    price_suggestion_currency_code,
                    price_total_amount,
                    price_total_currency_code,
                    price_shared_cost_amount,
                    price_shared_cost_currency_code,
                    area_range_size_from,
                    area_range_size_to,
                    area_range_unit,
                    area_range_description,
                    area_plot_size,
                    area_plot_unit,
                    area_plot_description,
                    organisation_name,
                    local_area_name,
                    number_of_bedrooms,
                    owner_type_description,
                    property_type_description,
                    viewing_times,
                    coordinates_lat,
                    coordinates_lon,
                    image_urls,
                    ad_link,
                    area_size,
                    area_unit,
                    area_description,
                    price_range_suggestion_amount_from,
                    price_range_suggestion_amount_to,
                    price_range_suggestion_currency_code,
                    price_range_total_amount_from,
                    price_range_total_amount_to,
                    price_range_total_currency_code,
                    bedrooms_range_start,
                    bedrooms_range_end
                ) VALUES (
                    :type,
                    :ad_id,
                    :main_search_key,
                    :heading,
                    :location,
                    :image_url,
                    :image_path,
                    :image_height,
                    :image_width,
                    :image_aspect_ratio,
                    :flags,
                    :styling,
                    :timestamp,
                    :logo_url,
                    :logo_path,
                    :price_suggestion_amount,
                    :price_suggestion_currency_code,
                    :price_total_amount,
                    :price_total_currency_code,
                    :price_shared_cost_amount,
                    :price_shared_cost_currency_code,
                    :area_range_size_from,
                    :area_range_size_to,
                    :area_range_unit,
                    :area_range_description,
                    :area_plot_size,
                    :area_plot_unit,
                    :area_plot_description,
                    :organisation_name,
                    :local_area_name,
                    :number_of_bedrooms,
                    :owner_type_description,
                    :property_type_description,
                    :viewing_times,
                    :coordinates_lat,
                    :coordinates_lon,
                    :image_urls,
                    :ad_link,
                    :area_size,
                    :area_unit,
                    :area_description,
                    :price_range_suggestion_amount_from,
                    :price_range_suggestion_amount_to,
                    :price_range_suggestion_currency_code,
                    :price_range_total_amount_from,
                    :price_range_total_amount_to,
                    :price_range_total_currency_code,
                    :bedrooms_range_start,
                    :bedrooms_range_end
                )
                """
                ),
                [vars(Doc(**utils.flattenDict(doc, mapper=lambda x: str(x)))) for doc in docs()],
            )
            conn.commit()


if __name__ == "__main__":
    from http.client import HTTPConnection

    HTTPConnection.debuglevel = 1

    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)

    # obtainRawIndexData()
    storeIndexData()
    # docAnalyze()

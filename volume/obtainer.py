import json
import utils
import classes
import logging
import os
import shutil
import random
from classes import Doc, FinnLocationFilter
import sqlalchemy as sa
from sqlalchemy import orm
import asyncio
import aiohttp
import config
import utils
from pprint import pprint
from typing import Generator, Iterable, Union
import tqdm

engine = sa.create_engine(config.SQL_ADDRESS, echo=False, future=True)
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)
mock = False

JsonValue = str | float | bool | dict | list
FinnFilterDict = dict[str, Union[JsonValue, "FinnFilterDict"]]


def getParams(page: int, **kwargs):
    return {
        "searchkey": "SEARCH_ID_REALESTATE_HOMES",
        "page": page,
        **kwargs
        # "lat": "60.386516342860716",
        # "lon": "5.32861852263332",
        # "radius": 8000,
        # "sort": "PUBLISHED_DESC",
        # "location": "1.22046.20220",
    }


def clearTempdir():
    if config.TMP_DIR.exists():
        shutil.rmtree(config.TMP_DIR)


def storeJsonInTempdir(response: dict, file: int):
    config.TMP_DIR.mkdir(exist_ok=True, parents=True)
    (config.TMP_DIR / file).write_text(json.dumps(response, indent=2))
    logger.info(f"Stored {config.TMP_DIR / file}")


async def getResponse(
    session: aiohttp.ClientSession,
    params: dict,
    sleepscale: int = 0,
    file: None | str = None,
):
    await asyncio.sleep(random.random() * sleepscale)

    if mock:
        with open(os.path.join("mock", "response.json"), "r") as f:
            responseJson = json.load(f)
    else:
        response = await session.request("GET", url=config.FINN_URL, params=params)
        responseJson = await response.json()

    if file:
        storeJsonInTempdir(responseJson, file)
    return responseJson


def filterGenerator(filters: Iterable[FinnFilterDict], maxDepth: float = float("inf")):
    mapFilterItems = lambda filters: (FinnLocationFilter(**f) for f in filters)

    def _filterGenerator(
        filters: Iterable[FinnLocationFilter], currDepth: int = 0
    ) -> Generator[FinnLocationFilter, None, None]:
        for f in filters:
            if (len(f.filter_items) == 0) or (currDepth == maxDepth):  # At bottom
                yield f
            else:
                yield from _filterGenerator(mapFilterItems(f.filter_items), currDepth + 1)

    yield from _filterGenerator(mapFilterItems(filters))


async def obtainRawIndexData():
    logger.info("Start obtainRawIndexData")
    clearTempdir()
    session = aiohttp.ClientSession()
    responseJson = await getResponse(session, {"searchkey": "SEARCH_ID_REALESTATE_HOMES", "page": 1})
    logger.info(f"Sucessfully obtained first response for metadata")
    locationFilters = utils.findFirst(responseJson["filters"], lambda x: x["name"] == "location")
    locationFilters = locationFilters["filter_items"]

    def taskGenerator(filter_: FinnLocationFilter, numberOfPages):
        for i in range(2, numberOfPages + 1):
            params = {
                "searchkey": "SEARCH_ID_REALESTATE_HOMES",
                "page": i,
                **filter_.getQueryParams(),
            }
            yield asyncio.create_task(
                getResponse(
                    session,
                    params,
                    sleepscale=numberOfPages * 0.1,
                    file=f"loc{filter_.display_name}_page{i}_{utils.isoNow()}.json",
                )
            )

    filters = tuple(filterGenerator(locationFilters, 1))
    logger.info(f"Distribute requests across {len(filters)} filters")
    for i, filter_ in enumerate(filters):
        params = {"searchkey": "SEARCH_ID_REALESTATE_HOMES", "page": 1, **filter_.getQueryParams()}
        responseJson = await getResponse(
            session, params, file=f"loc{filter_.display_name}_page1_{utils.isoNow()}.json"
        )

        logger.info(
            f"Sucessfully obtained first response with filter {filter_.display_name}, {filter_.value}"
        )

        logger.info(
            f"Now doing requests for filter ({i}/{len(filters)}): {filter_.display_name}, {filter_.value}"
        )
        await asyncio.gather(*taskGenerator(filter_, responseJson["metadata"]["paging"]["last"]))
    await session.close()


def storeIndexData():
    """
    Assumes index data is available (generated from obtainRawIndexData)
    """
    session: orm.Session
    with orm.Session(engine) as session:
        session.delete(Doc)
    with orm.Session(engine) as session:
        session.add_all(Doc(**utils.flattenDict(doc, mapper=str)) for doc in utils.docs())
        session.commit()


if __name__ == "__main__":
    # from http.client import HTTPConnection

    # HTTPConnection.debuglevel = 1

    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)

    # asyncio.run(obtainRawIndexData())
    storeIndexData()

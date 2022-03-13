import json
import utils
import classes
import logging
import os
import shutil
import random
from classes import Doc
import sqlalchemy as sa
from sqlalchemy import orm
import asyncio
import aiohttp
import config
import utils

engine = sa.create_engine(config.SQL_ADDRESS, echo=False, future=True)
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def getParams(page: int):
    return {
        "searchkey": "SEARCH_ID_REALESTATE_HOMES",
        "page": page,
        # "lat": "60.386516342860716",
        # "lon": "5.32861852263332",
        # "radius": 8000,
        # "sort": "PUBLISHED_DESC",
        # "location": "1.22046.20220",
    }


def clearTempdir():
    if config.TMP_DIR.exists():
        shutil.rmtree(config.TMP_DIR)


def storeResponseInTempdir(response: dict, page: int):
    config.TMP_DIR.mkdir(exist_ok=True, parents=True)
    filename = f"response_page{page}_{utils.isoNow()}.json"
    (config.TMP_DIR / filename).write_text(json.dumps(response, indent=2))
    logger.info(f"Stored response {config.TMP_DIR / filename}")


async def getAndStoreResponse(
    session: aiohttp.ClientSession, params: dict, mock: bool = False, sleepscale: int = 5
):
    await asyncio.sleep(random.random() * sleepscale)
    logger.debug(f"getResponse with params: {params}")
    if mock:
        with open(os.path.join("mock", "response.json"), "r") as f:
            return json.load(f)
    response = await session.request("GET", url=config.FINN_URL, params=params)
    responseJson = await response.json()
    storeResponseInTempdir(responseJson, params["page"])
    return responseJson


async def obtainRawIndexData():
    logger.info("Start obtainRawIndexData")
    clearTempdir()
    session = aiohttp.ClientSession()
    responseJson = await getAndStoreResponse(session, getParams(1))
    logger.info(f"Sucessfully obtained first response")
    paging = classes.Paging(**responseJson["metadata"]["paging"])
    numberOfPages = paging.last
    logger.info(f"Total number of pages: {numberOfPages}")
    await asyncio.gather(
        *(
            asyncio.create_task(
                getAndStoreResponse(session, getParams(i), sleepscale=numberOfPages * 0.075)
            )
            for i in range(2, numberOfPages + 1)
        )
    )
    await session.close()


def storeIndexData():
    """
    Assumes index data is available (generated from obtainRawIndexData)
    """
    session: orm.Session
    with orm.Session(engine) as session:
        session.add_all(Doc(**utils.flattenDict(doc, mapper=str)) for doc in utils.docs())
        session.commit()


if __name__ == "__main__":
    # from http.client import HTTPConnection

    # HTTPConnection.debuglevel = 1

    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)

    asyncio.run(obtainRawIndexData())
    storeIndexData()

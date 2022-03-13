import json
from typing import Iterable
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
from sqlalchemy import orm
import asyncio
import aiohttp

engine = sa.create_engine("sqlite:///test.db", echo=False, future=True)

TMP_DIR = pathlib.Path("data") / "indexjsons"

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


def storeResponseInTempdir(response: dict, page: int):
    TMP_DIR.mkdir(exist_ok=True, parents=True)
    # filename = "response_" + "page_" + utils.isoNow() + ".json"
    filename = f"response_page{page}_{utils.isoNow()}.json"
    (TMP_DIR / filename).write_text(json.dumps(response, indent=2))
    logger.info(f"Stored response {TMP_DIR / filename}")


async def getResponse(
    session: aiohttp.ClientSession, params: dict, mock: bool = False, sleepscale: int = 5
):
    await asyncio.sleep(random.random() * sleepscale)
    logger.debug(f"getResponse with params: {params}")
    if mock:
        with open(os.path.join("mock", "response.json"), "r") as f:
            return json.load(f)
    response = await session.request("GET", url=URL, params=params)
    responseJson = await response.json()
    storeResponseInTempdir(responseJson, params["page"])
    return responseJson


async def obtainRawIndexData():
    logger.info("Start obtainRawIndexData")
    clearTempdir()
    session = aiohttp.ClientSession()
    responseJson = await getResponse(session, getParams(1))
    logger.info(f"Sucessfully obtained first response")
    paging = classes.Paging(**responseJson["metadata"]["paging"])
    numberOfPages = paging.last
    logger.info(f"Total number of pages: {numberOfPages}")
    await asyncio.gather(
        *(
            asyncio.create_task(getResponse(session, getParams(i), sleepscale=numberOfPages * 0.075))
            for i in range(2, numberOfPages + 1)
        )
    )
    await session.close()


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
    session: orm.Session
    with orm.Session(engine) as session:
        session.add_all(Doc(**utils.flattenDict(doc, mapper=str)) for doc in docs())
        session.commit()


if __name__ == "__main__":
    from http.client import HTTPConnection

    # HTTPConnection.debuglevel = 1

    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)

    asyncio.run(obtainRawIndexData())
    storeIndexData()
    # docAnalyze()

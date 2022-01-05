import json
import requests
import utils
import classes
import time
import logging
import sys
import tempfile
import os
import pathlib
import shutil
import random

TMP_DIR = pathlib.Path(tempfile.gettempdir()) / "apartmentscience" / "indexjsons"

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.INFO)

URL = "https://www.finn.no/api/search-qf"
params = {
    "searchkey": "SEARCH_ID_REALESTATE_HOMES",
    "lat": "60.386516342860716",
    "lon": "5.32861852263332",
    "radius": 8000,
    "sort": "PUBLISHED_DESC",
    "location": "1.22046.20220",
    "page": 2,
}


def getParams(page: int):
    return {
        "searchkey": "SEARCH_ID_REALESTATE_HOMES",
        "lat": "60.386516342860716",
        "lon": "5.32861852263332",
        "radius": 8000,
        "sort": "PUBLISHED_DESC",
        "location": "1.22046.20220",
        "page": page,
    }


def clearTempdir():
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)


def storeResponseInTempdir(response: dict):
    TMP_DIR.mkdir(exist_ok=True)
    filename = "response" + utils.isoNow() + ".json"
    (TMP_DIR / filename).write_text(json.dumps(response, indent=2))
    logger.info(f"Stored response {filename} in {TMP_DIR}")


def getResponse(params: dict, mock: bool = False):
    if mock:
        with open("response.json", "r") as f:
            responseJson = json.load(f)
    else:
        response = requests.get(URL, params)
        responseJson = response.json()
    return responseJson


def obtainRawData():
    responseJson = getResponse(getParams(1))
    logger.info("Start obtainRawData")

    # utils.jprint(responseJson, "response.json")
    logger.info(f"Sucessfully obtained first response")
    logger.debug(responseJson)

    clearTempdir()
    storeResponseInTempdir(responseJson)

    paging = classes.Paging(**responseJson["metadata"]["paging"])
    numberOfPages = paging.last
    logger.info(f"Total number of pages: {numberOfPages}")
    for i in range(2, numberOfPages + 1):
        params = getParams(i)
        logger.debug(f"{params}")

        responseJson = getResponse(params, False)
        logger.debug(responseJson)
        storeResponseInTempdir(responseJson)

        waitTime = 0.2 + random.random()
        logger.info(f"Waiting {waitTime}s before next call")
        time.sleep(waitTime)


if __name__ == "__main__":
    obtainRawData()

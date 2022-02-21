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
from pprint import pprint

TMP_DIR = pathlib.Path("data") / "apartmentscience" / "indexjsons"

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

URL = "https://www.finn.no/api/search-qf"


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


def obtainRawDetailedData():
    """
    Assumes index data is available (generated from obtainRawIndexData)
    """
    for file in os.listdir(TMP_DIR):
        with open(os.path.join(TMP_DIR, file), "r") as f:
            index = json.load(f)


if __name__ == "__main__":
    from http.client import HTTPConnection

    HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)

    obtainRawIndexData()
    # obtainRawDetailedData()

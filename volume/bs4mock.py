import json
from pprint import pprint
import os
from bs4 import BeautifulSoup, element
import textUtils
import re
import string

dirpath = "data/apartmentscience/indexjsons/"
files = os.listdir(dirpath)

with open(dirpath + files[0], "r") as f:
    index = json.load(f)

url = index["docs"][0]["ad_link"]
print(url)
print(index["docs"][0])
# resp = requests.get(url)

# with open('test.html', 'w+') as f:
#     f.write(resp.content.decode(resp.encoding))

with open("test.html", "r") as f:
    html = f.read()

bs = BeautifulSoup(html, "html.parser")
dls = bs.find_all("dl")


def dictFromDls(dls: element.ResultSet) -> dict[str, str]:
    """
    Converts a ResultSet of dl-tags to a dictionary
    Example
    -------
    >>> getDictFromDls(bs.find_all('dl'))
    """
    result = {}
    for dl in dls:
        dts: element.ResultSet = dl.find_all("dt")
        dds: element.ResultSet = dl.find_all("dd")
        for dt, dd in zip(dts, dds):
            result[dt.text] = dd.text
    return result


res = dictFromDls(dls)
pprint(res)


class Features:
    """
    Class of constants containing name of raw features, and also the target feature names
    """

    class raw:
        BEDROOMS = "Soverom"
        ENERGY_RATING = "Energimerking"
        MUNICIPAL_TAXES = "Kommunale avg."
        PLOT_AREA = "Tomteareal"
        PRICE_ESTIMATE = "Prisantydning"
        PRIMARY_AREA = "Primærrom"
        PROPERTY_VALUE = "Formuesverdi"
        TOTAL_PRICE = "Totalpris"
        TRANSER_COST = "Omkostninger"
        USABLE_AREA = "Bruksareal"
        YEAR_OF_CONSTRUCTION = "Byggeår"

    class target:
        BEDROOMS = "bedrooms"
        ENERGY_RATING = "energyRating"
        MUNICIPAL_TAXES = "municipalTaxes"
        PLOT_AREA = "plotArea"
        PRICE_ESTIMATE = "priceEstimate"
        PRIMARY_AREA = "primaryArea"
        PROPERTY_VALUE = "propertyValue"
        TOTAL_PRICE = "totalPrice"
        TRANSER_COST = "transferCost"
        USABLE_AREA = "usableArea"
        YEAR_OF_CONSTRUCTION = "yearOfConstruction"


def processDlDict(dl: dict):
    extractIntFrom = (
        Features.raw.BEDROOMS,
        Features.raw.MUNICIPAL_TAXES,
        Features.raw.PLOT_AREA,
        Features.raw.PRIMARY_AREA,
        Features.raw.PROPERTY_VALUE,
        Features.raw.TOTAL_PRICE,
        Features.raw.TRANSER_COST,
        Features.raw.USABLE_AREA,
        Features.raw.YEAR_OF_CONSTRUCTION,
    )
    result = {}
    for key in extractIntFrom:
        result[key] = (val := dl.get(key, None) or None) and textUtils.extractInt(val)
    energyRatingMap = {a: i for i, a in enumerate(string.ascii_uppercase[6::-1])}
    match = re.search("[A-Z]", dl.get(Features.raw.ENERGY_RATING, ""))
    result[Features.raw.ENERGY_RATING] = match and energyRatingMap[match.group()]
    pprint(result)


processDlDict(res)

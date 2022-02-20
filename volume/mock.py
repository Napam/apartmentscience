import json
import requests
from pprint import pprint
import os 
from bs4 import BeautifulSoup, element
import textUtils
import re

dirpath = 'data/apartmentscience/indexjsons/'
files = os.listdir(dirpath)

with open(dirpath + files[0], 'r') as f:
    thing = json.load(f)

url = thing['docs'][0]['ad_link']
print(url)
# resp = requests.get(url)

# with open('test.html', 'w+') as f:
#     f.write(resp.content.decode(resp.encoding))

with open('test.html', 'r') as f:
    html = f.read()

bs = BeautifulSoup(html, 'html.parser')
dls = bs.find_all('dl')

def dictFromDls(dls: element.ResultSet) -> dict[str, str]:
    '''
    Converts a ResultSet of dl-tags to a dictionary
    Example
    -------
    >>> getDictFromDls(bs.find_all('dl'))
    '''
    result = {}
    for dl in dls:
        dts: element.ResultSet = dl.find_all('dt')
        dds: element.ResultSet = dl.find_all('dd')
        for dt, dd in zip(dts, dds):
            result[dt.text] = dd.text
    return result

res = dictFromDls(dls)
pprint(res)

class Features:
    USABLE_AREA = 'Bruksareal'
    YEAR_OF_CONSTRUCTION = 'Byggeår'
    PROPERTY_VALUE = 'Formuesverdi'
    MUNICIPAL_TAXES = 'Kommunale avg.'
    TRANSER_COST = 'Omkostninger'
    PRIMARY_AREA = 'Primærrom'
    BEDROOMS = 'Soverom'
    PLOT_AREA = 'Tomteareal'
    TOTAL_PRICE = 'Totalpris'

def processDlDict2(dl: dict):
    extractIntFrom = (
        'Bruksareal', 
        'Byggeår', 
        'Formuesverdi', 
        'Kommunale avg.',
        'Omkostninger',
        'Primærrom',
        'Soverom',
        'Tomteareal',
        'Totalpris',
        'AAA'
    )
    energyRatingKey = 'Energimerking'

    result = {}
    for key in extractIntFrom:
        result[key] = (val := dl.get(key, None)) and int(textUtils.extractNumber(val))

    energyRatingMap = {
        'A': 6,
        'B': 5,
        'C': 4,
        'D': 3,
        'E': 2,
        'F': 1,
        'G': 0,
    }

    match = re.search('[A-Z]', dl.get(energyRatingKey, ''))
    result[energyRatingKey] = match and energyRatingMap[match.group()]

    pprint(result)

processDlDict2(res)
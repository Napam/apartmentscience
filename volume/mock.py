import json
import requests
import os 
from bs4 import BeautifulSoup

dirpath = 'data/apartmentscience/indexjsons/'
files = os.listdir(dirpath)

with open(dirpath + files[0], 'r') as f:
    thing = json.load(f)

url = thing['docs'][0]['ad_link']
resp = requests.get(url)

with open('test.html', 'w+') as f:
    f.write(resp.content.decode(resp.encoding))

with open('test.html', 'r') as f:
    html = f.read()

bs = BeautifulSoup(html, 'html.parser')
print(bs.find('dl', class_='definition-list definition-list--cols1to2').find_all('dd'))
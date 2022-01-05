import json
import utils

with open('response.json', 'r') as f:
    responseData = json.load(f)

utils.jprint(responseData['metadata']['paging'])
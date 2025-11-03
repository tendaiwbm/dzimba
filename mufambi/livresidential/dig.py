import time
import json
import requests as rq

from .model import LIVResidentialModel as model
from .config import LivResidentialConfig as source
from ..utils import *


def parse_response(payload):
    def parse_listing(listing):
        listing = listing["_formatted"]
        return {
                 "_id": "-".join([listing["address_1"].replace(",","").replace(" ","-").lower(),listing["id"]]),
                 "url": create_path([listing["slug_city"],listing["slug_neighborhood"],listing["slug_street"]])
               }

    return list(map(parse_listing,payload))

def request(url,params,headers):
    
    payload = []
    request = rq.post(url,data=json.dumps(params),headers=headers)
        
    try:    assert request.status_code == 200
    except: return payload
        
    response = request.json()
    
    try: assert "hits" in response
    except: return payload
    
    return response["hits"]

def pipeline():
    pipelineSetup = {
                      "request": {"function": request, "args": [source["dataUrl"],source["requestParams"],source["headers"]]},
                      "parser": parse_response,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["domain"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": False
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()


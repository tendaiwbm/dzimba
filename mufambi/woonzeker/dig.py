import requests as rq

from .model import WoonzekerModel as model
from .config import WoonzekerConfig as source
from ..utils import *

def parse_response(payload):
    def parse_listing(listing):
        return {
                 "_id": listing["id"],
                 "url": create_path(["",listing["slug"]]),
                 "status": listing["status"]["label"],
                 "viewers": listing["statistics"]["inquiries"]
               }

    return list(map(parse_listing,payload))

def request(url):
    request = rq.get(url)

    try:
        response = request.json()
    except:
        return

    if not(response["data"]): 
        return
    else:
        return response["data"]

def pipeline():
    pipelineSetup = {
                      "request": {"function": request, "args": [source["dataUrl"]]},
                      "parser": parse_response,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["host"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": source["filters"]
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()

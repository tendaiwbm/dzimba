import logging

logger = logging.getLogger("RentalRotterdam")

import requests as rq
import pandas as p

from bs4 import BeautifulSoup as BTSP

from .model import RentalRotterdamModel as model
from .config import rentalRotterdamConfig as source
from ..utils import *

def dom_articles_to_json(dom):
    def dom_article_to_json(article):
        listingData = article.find_all(attrs={"class": "object__data"})[0]
        price = listingData.find_all(attrs={"class": "price"})[0].text.replace("€","").strip().split(",")[0]
        identifier = listingData.find_all(attrs={"class":"object__address-container"})[0].attrs["href"].split("?")[0]
        energyLabel = listingData.find_all(attrs={"class": "object_energyclass"}) 

        return {
                 "_id": "-".join(identifier.split("/")[-2:]),
                 "url": identifier,
                 "price": int(price) if "." not in price else int(float(price)*1000),
                 "city": listingData.find_all(attrs={"class": "locality"})[0].text.strip(),
                 "energyLabel": energyLabel[0].text.strip() if energyLabel else None 
               }

    dom = BTSP(dom,"html.parser").find_all("article")
    return list(map(dom_article_to_json,dom))

def request(url,params):
    try:
        assert params["skip"] == 0
    except:
        params["skip"] = 0

    pageFound = True
    payload = []
    while pageFound:
        request = rq.post(url,data=params)
        
        try:    assert request.status_code == 200
        except: break
        
        response = request.text
        pageFound = "Geen objecten gevonden" not in str(response)
        
        if not(pageFound): break

        payload.append(response)
        params["skip"] += params["take"]
    
    return payload

def parse_response(payload):
    response = map(dom_articles_to_json,payload)
    return [listing for subList in response for listing in subList]
    
def pipeline():  
    pipelineSetup = {
                      "request": {
                                   "function": request,
                                   "args": [
                                             create_path([source["domain"],source["endpoint"]]),
                                             source["requestParams"]
                                           ]
                                 },
                      "parser": parse_response,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["domain"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": source["filters"],
                      "logger": logger
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()
